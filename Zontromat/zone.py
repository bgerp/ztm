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
import os

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

from services.http.server import Server
from services.http.register_handler import RegisterHandler
from services.evok.settings import EvokSettings
from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

    __server = None
    """Self hosting for EVOK WEB hooks."""

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

        # Take PLC info from settings.
        vendor = self.__app_settings.get_controller["vendor"]
        model = self.__app_settings.get_controller["model"]
        serial = 0

        # Read PLC information.
        plc_info = ControllerFactory.get_info()

        if "serial" in plc_info:
            if plc_info["serial"] is not None:
                serial = plc_info["serial"]

        if "model" in plc_info:
            if plc_info["model"] is not None:
                model = plc_info["model"]

        # TODO: To be scaled when get time for 1 minute intrval.
        self.__update_timer.expiration_time = self.__update_timer.expiration_time + (serial / 1000)

        # Create Neuron.
        config = {
            "vendor": vendor,
            "model": model,
            "serial": serial,
            "host": self.__app_settings.get_controller["host"],
            "timeout": self.__app_settings.get_controller["timeout"]
        }

        self.__controller = ControllerFactory.create(config)

        # Create bgERP and login.
        self.__bgerp = bgERP(self.__app_settings.get_erp_service["host"],\
            self.__app_settings.get_erp_service["timeout"])
        self.__erp_service_update_timer = Timer(self.__erp_service_update_rate)

        # Set the plugin manager.
        self.__plugin_manager = PluginsManager(self.__registers, self.__controller)

        # Set the performance profiler.
        self.__performance_profiler.enable_mem_profile = self.__app_settings.ram_usage
        self.__performance_profiler.enable_time_profile = self.__app_settings.run_time_usage
        self.__performance_profiler.on_time_change(self.__on_time_change)
        self.__performance_profiler.on_memory_change(self.__on_memory_change)

        # Setup the performance profiler timer.
        self.__performance_profiler_timer = Timer(60000)

        # Create WEB service.
        if os.name == "posix":
            
            # Create entrance
            evok_settings = EvokSettings("/etc/evok.conf")
            
            # Setup the EVOK web hooks.
            evok_settings.webhook_enabled = True
            evok_settings.webhook_address = "http://127.0.0.1:8889/api/evok-webhooks   ; Put your server endpoint address here (e.g. http://123.123.123.123:/wh )"
            evok_settings.webhook_device_mask = ["input", "wd"]
            evok_settings.webhook_complex_events = True
            
            # Save
            evok_settings.save()

            # Restart the service to accept the settings.
            EvokSettings.restart()

            # Create the WEB server.
            self.__server = Server("127.0.0.1", 8889)

        if os.name == "nt":
            # self.__server = Server("176.33.1.207", 8889)
            self.__server = Server("192.168.100.2", 8889)

        # Set the IO map.
        gpio_map = self.__controller.get_gpio_map()
        RegisterHandler.set_gpio_map(gpio_map)

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

            GlobalErrorHandler.log_no_connection_plc(self.__logger)

            self.__controller_comm_failures += 1
            if self.__controller_comm_failures >= 30:
                self.__controller_comm_failures = 0

                # Restart service
                # if os.name == "posix":
                #     os.system("sudo service EVOK restart")

                # In case of failure:
                # - Try several times if result is still unsuccessful reestart the EVOK.
                # - Wait EVOK service to start.
                # - Continue main cycle.

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

        # Start the server.
        if not self.__server.is_alive:
            self.__server.start()

        # Update the neuron.
        state = self.__controller.update()

        if state == UpdateState.Success:
            self.__controller_comm_failures = 0

        elif state == UpdateState.Failure:
            self.__controller_comm_failures += 1
            if self.__controller_comm_failures >= 20:
                self.__controller_comm_failures = 0

                self.__logger.error("EVOK service should be restarted.")

            GlobalErrorHandler.log_no_connection_plc(self.__logger)

        # Give plugins runtime.
        self.__plugin_manager.update()

        # Update periodically bgERP.
        self.__erp_service_update_timer.update()
        if self.__erp_service_update_timer.expired:
            self.__erp_service_update_timer.clear()

            ztm_regs = self.__registers.by_source(Source.Zontromat)
            ztm_regs = ztm_regs.new_then(60)                
            ztm_regs_dict = ztm_regs.to_dict()

            update_state = self.__bgerp.sync(ztm_regs_dict)

            if update_state is not None:
                self.__registers.update(update_state)

            else:
                GlobalErrorHandler.log_no_connection_erp(self.__logger)


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

        time_usage = self.__registers.by_name("sys.time.usage")
        if time_usage is not None:
            time_usage.value = passed_time

        # print(f"Total time: {passed_time:06.3f} sec")

    def __on_memory_change(self, current, peak):

        ram_current = self.__registers.by_name("sys.ram.current")
        if ram_current is not None:
            ram_current.value = current

        ram_peak = self.__registers.by_name("sys.ram.peak")
        if ram_peak is not None:
            ram_peak.value = peak

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
                    # self.__zone_state.set_state(ZoneState.Init)

                self.__busy_flag = False

    def shutdown(self):
        """Shutdown the process."""

        # Stop the server.
        if self.__server.is_alive:
            self.__server.stop()

        self.__zone_state.set_state(ZoneState.Shutdown)
        self.__plugin_manager.shutdown()
        self.__stop_flag = True

#endregion
