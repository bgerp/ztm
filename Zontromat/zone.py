#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""

Zontromat - Zonal Electronic Automation

Copyright (C) [2020] [POLYGONTeam Ltd.]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""

import traceback

from enum import Enum

from utils.settings import ApplicationSettings
from utils.logger import get_logger
from utils.state_machine import StateMachine
from utils.timer import Timer
#from utils.utils import time_usage, mem_usage, mem_time_usage
from utils.performance_profiler import PerformanceProfiler

from controllers.controller_factory import ControllerFactory
from controllers.update_state import UpdateState

from bgERP.bgERP import bgERP

from data.register import Register, Source, Scope
from data.registers import Registers

from plugins.plugins_manager import PluginsManager

# from controllers.neuron.neuron.read_eeprom

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "or.dimitrov@polygonteam.com"
"""E-mail of the author.
@see or.dimitrov@polygonteam.com"""

__status__ = "Debug"
"""File status."""

#endregion

class EnergyMode(Enum):
    """Energy mode.
        @see Zontromat document
    """

    Peak = 0 # peak (върхов)
    Normal = 1 # normal (нормален)
    Accumulate = 2 # accumulate (акумулиране)
    Generator = 3 # generator (на генератор)

class EmergencyMode:
    """Energy mode enumeration.
        @see Zontromat document
    """
    Normal = 0 # normal (0) - Нормално опериране
    Fire = 1 # isFire (1) - има пожар в сградата
    Storm = 2 # isStorm (2) - има буря около сградата
    Earthquake = 4 # isEarthquake (4) - има земетресение
    Gassing = 8 # isGassing (8) - има обгазяване около сградата
    Flooding = 16 # isFlooding (16) - има наводнение около сградата
    Blocked = 32 # isBlocked (32) - сградата е блокирана

class ZoneState(Enum):
    """Zone state machine flags."""

    Idle = 0
    Init = 1
    Login = 2
    Run = 3
    Shutdown = 4
    Test = 5

class Zone():
    """Main zone class"""

#region Attributes

    __app_settings = None
    """Application settings."""

    __zone_state = ZoneState.Idle
    """Zone state."""

    __logger = None
    """Logger"""

    __controller = None
    """Neuron controller."""

    __bgerp = None
    """Communication with bgERP."""

    __registers = None
    """Registers"""

    __plugin_manager = None
    """Plugin manager."""

    __update_rate = 0.5
    """Controlling update rate in seconds."""

    __update_timer = None
    """Update timer."""

    __erp_service_update_rate = 5
    """ERP service update rate in seconds."""

    __erp_service_update_timer = None
    """ERP update timer."""

    __zone_state = None
    """Zone state."""

    __stop_flag = False
    """Time to Stop flag."""

    __busy_flag = False
    """Busy flag."""

    __controller_comm_failures = 0
    """Controller communication failures."""

    __performance_profiler = PerformanceProfiler()
    """Performance profiler."""

    __performance_profiler_timer = None
    """Performance profiler timer."""

#endregion

#region Constructor

    def __init__(self):
        """Init the process."""

        # Application settings.
        self.__app_settings = ApplicationSettings.get_instance()

        # Create logger.
        self.__logger = get_logger(__name__)

        # Create registers.
        self.__registers = Registers.get_instance()

        # Update timer.
        self.__update_timer = Timer(self.__update_rate)

        # Set zone state machine.
        self.__zone_state = StateMachine(ZoneState.Idle)
        self.__zone_state.on_change(self.__cb_zone_state)

        # Create Neuron.
        config = {
            "vendor": self.__app_settings.get_controller["vendor"],
            "model":  self.__app_settings.get_controller["model"],
            "host": self.__app_settings.get_controller["host"],
            "timeout": self.__app_settings.get_controller["timeout"]
        }
        self.__controller = ControllerFactory.create(config)

        # Create bgERP and login.
        self.__bgerp = bgERP(self.__app_settings.get_erp_service["host"],\
            self.__app_settings.get_erp_service["timeout"])
        self.__erp_service_update_timer = Timer(self.__erp_service_update_rate)

        # Set the plugin manager.
        self.__plugin_manager = PluginsManager(self.__registers, self.__controller, self.__bgerp)

        # Set the performance profiler.
        self.__performance_profiler.enable_mem_profile = self.__app_settings.ram_usage
        self.__performance_profiler.enable_time_profile = self.__app_settings.run_time_usage
        self.__performance_profiler.on_time_change(self.__on_time_change)
        self.__performance_profiler.on_memory_change(self.__on_memory_change)

        register = Register("self.ram.current")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("self.ram.peak")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("self.time.usage")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        # Setup the performance profiler timer.
        self.__performance_profiler_timer = Timer(60000)

#endregion

#region Private Methods

    def __cb_zone_state(self, machine):
        """Set zone state."""

        self.__logger.info("Zone state: {}".format(machine.get_state()))

    def __init(self):
        """Init the zone."""

        # Update the neuron.
        state = self.__controller.update()

        if state == UpdateState.Success:

            # Clear all resources.
            self.__zone_state.set_state(ZoneState.Login)

        elif state == UpdateState.Failure:

            self.__controller_comm_failures += 1
            if self.__controller_comm_failures >= 10:
                self.__controller_comm_failures = 0

                # Restart service
                # if os.name == "posix":
                #     os.system("sudo service EVOK restart")

                """
                TODO: In case of failure:
                - Try several times if result is still unsuccessful reestart the EVOK.
                - Wait EVOK service to start.
                - Continue main cycle.
                """

                message = "Communication lost with controller."
                self.__logger.error(message)

            self.__zone_state.set_state(ZoneState.Init)

    def __login(self):
        """Login to bgERP."""

        # one_wire = self.__controller.get_1w_devices()
        # modbus = self.__controller.get_modbus_devices()
        credentials = \
        { \
            "serial_number": self.__controller.serial_number, \
            "model": self.__controller.model, \
            "version": self.__controller.version, \
            "config_time": self.__app_settings.get_erp_service["config_time"], \
            # "one_wire": one_wire, \
            # "modbus": modbus, \
        }

        login_state = self.__bgerp.login(credentials)

        if login_state:
            self.__zone_state.set_state(ZoneState.Run)
        else:
            self.__zone_state.set_state(ZoneState.Init)

    def __run(self):

        # Update the neuron.
        state = self.__controller.update()

        if state == UpdateState.Success:
            self.__plugin_manager.update()
            self.__controller_comm_failures = 0

        elif state == UpdateState.Failure:
            self.__controller_comm_failures += 1
            if self.__controller_comm_failures >= 10:
                self.__controller_comm_failures = 0

                self.__logger.error("EVOK service should be restarted.")
                """
                TODO: In case of failure:
                - Try several times if result is still unsuccessful reestart the EVOK.
                - Wait EVOK service to start.
                - Continue main cycle.
                - Tell bgERP that the EVOK is not runing.
                """

            self.__logger.error("Module {} Communication lost with EVOK.".format(__name__))

        # Update periodically bgERP.
        self.__erp_service_update_timer.update()
        if self.__erp_service_update_timer.expired:
            self.__erp_service_update_timer.clear()

            try:
                ztm_regs = self.__registers.by_source(Source.Zontromat)
                ztm_regs_dict = ztm_regs.to_dict()
                update_state = self.__bgerp.sync(ztm_regs_dict)

                if update_state is not None:
                    self.__registers.update(update_state)

                else:
                    pass
                    # self.__logger.error("Unsuccessful update to ERP service.")
                    # Pass it is not necessary to restart everything.
                    # self.__zone_state.set_state(ZoneState.Init)

            except Exception as e:
                self.__logger.error("No connection to the ERP service.")

    def __shutdown(self):
        """Shutdown procedure."""

        self.__plugin_manager.shutdown()
        self.__stop_flag = True

    def __test(self):
        """Test devices."""

        success = True

        if success:
            self.__zone_state.set_state(ZoneState.Run)

        else:
            self.__zone_state.set_state(ZoneState.Test)

    def __on_time_change(self, passed_time):
        register = self.__registers.by_name("self.time.usage")
        register.value = passed_time
        # print(f"Total time: {passed_time:06.3f} sec")

    def __on_memory_change(self, current, peak):
        register = self.__registers.by_name("self.ram.current")
        register.value = current
        register = self.__registers.by_name("self.ram.peak")
        register.value = peak
        # print(f"Current memory usage is {current / 10**3}kB; Peak was {peak / 10**3}kB")

    @__performance_profiler.profile
    def __update(self):

        if self.__zone_state.is_state(ZoneState.Idle):
            # Do nothing for now.
            self.__zone_state.set_state(ZoneState.Init)

        elif self.__zone_state.is_state(ZoneState.Init):
            # Initialize
            self.__init()

        elif self.__zone_state.is_state(ZoneState.Login):
            # Login room.
            self.__login()

        elif self.__zone_state.is_state(ZoneState.Run):
            # Run the process of the room.
            self.__run()

        elif self.__zone_state.is_state(ZoneState.Shutdown):
            # Shutdown the devices.
            self.__shutdown()

        elif self.__zone_state.is_state(ZoneState.Test):
            self.__test()

#endregion

#region Public Methods

    def run(self):
        """Run the process."""

        while not self.__stop_flag:

            # Update process timers.
            self.__update_timer.update()
            self.__performance_profiler_timer.update()

            # If time has come for execution then run it once and clear the timer.
            if self.__update_timer.expired:
                self.__update_timer.clear()


                # If the busy flag is raise pass the update cycle.
                if self.__busy_flag:
                    pass

                self.__busy_flag = True

                try:
                    # If the time has come for profiling.
                    # Enable the flag and tke profile.
                    if self.__performance_profiler_timer.expired:
                        self.__performance_profiler_timer.clear()
                        self.__performance_profiler.enable = True

                    # Update the application.
                    self.__update()

                    # If the performance profile is runing stop it after the cycle.
                    if self.__performance_profiler.enable:
                        self.__performance_profiler.enable = False

                # Log the exception without to close the application.
                except Exception:
                    self.__logger.error(traceback.format_exc())
                    self.__zone_state.set_state(ZoneState.Init)

                self.__busy_flag = False

    def shutdown(self):
        """Shutdown the process."""

        self.__zone_state.set_state(ZoneState.Shutdown)
        self.__plugin_manager.shutdown()
        self.__stop_flag = True

#endregion
