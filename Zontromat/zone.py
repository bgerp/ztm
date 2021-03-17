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

import sys
import traceback
import os
import queue

from enum import Enum

from utils.settings import ApplicationSettings
from utils.logger import get_logger
from utils.performance_profiler import PerformanceProfiler

from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer
from controllers.controller_factory import ControllerFactory

from bgERP.bgERP import bgERP

from data.register import Scope
from data.registers import Registers

from plugins.plugins_manager import PluginsManager

from services.evok.settings import EvokSettings
from services.global_error_handler.global_error_handler import GlobalErrorHandler

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov"]
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

    __logger = None
    """Logger"""

    __app_settings = None
    """Application settings."""

    __controller = None
    """Neuron controller."""

    __erp = None
    """Communication with the ERP."""

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

    __performance_profiler = PerformanceProfiler()
    """Performance profiler."""

    __performance_profiler_timer = None
    """Performance profiler timer."""

    # (Request to stop the queue from MG @ 15.01.2021)
    # __registers_snapshot = None
    # """Registers snapshot."""

#endregion

#region Constructor

    def __init__(self):
        """Init the zone."""

        pass

#endregion

#region Private Methods

    def __init_runtime(self):

        # Set the performance profiler.
        self.__performance_profiler.enable_mem_profile = True
        self.__performance_profiler.enable_time_profile = True
        self.__performance_profiler.on_time_change(self.__on_time_change)
        self.__performance_profiler.on_memory_change(self.__on_memory_change)

        # Setup the performance profiler timer. (60) 10 is for tests.
        self.__performance_profiler_timer = Timer(10)


        # Set zone state machine.
        self.__zone_state = StateMachine()
        self.__zone_state.on_change(self.__cb_zone_state)
        self.__zone_state.set_state(ZoneState.Idle)

        # Update timer.
        self.__update_timer = Timer(self.__update_rate)
            
        # Update with offset based on the serial number of the device.
        time_offset = 0
        if self.__controller.serial_number is not None and self.__controller.serial_number.isdigit():
            time_offset = int(self.__controller.serial_number)
        self.__update_timer.expiration_time = self.__update_timer.expiration_time + (time_offset / 1000)


    def __init_registers(self):
        """Setup registers source.
        """

        if os.name == "posix":
            file_path = os.path.join("..", "registers.csv")
            self.__registers = Registers.from_CSV(file_path)

        elif os.name == "nt":
            self.__registers = Registers.from_CSV("registers.csv")


    def __evok_cb(self, device):
        """EVOK callback service handler.

        Args:
            device (JSON): GPIOs that was changed.
        """

        # Target inputs, by registers names.
        names = ["ac.door_closed_1.input", "ac.door_closed_2.input",\
            "ac.pir_1.input", "ac.pir_2.input",\
            "ac.window_closed_1.input", "ac.window_closed_2.input",\
            "monitoring.cw.input", "monitoring.hw.input", "sys.at.input"]
        inputs = self.__registers.by_names(names)
        gpio = self.__controller.device_to_uniname(device)

        for input_reg in inputs:
            if input_reg is not None:
                if input_reg.value == gpio:

                    # If register exists, apply value.
                    required_name = input_reg.name.replace("input", "state")
                    target_reg = self.__registers.by_name(required_name)
                    if target_reg is not None:
                        target_reg.value = device["value"]

    def __init_controller(self):
        """Init the controller.
        """

        # Create PLC.
        self.__controller = ControllerFactory.create(self.__app_settings.controller)

        if self.__controller is None:
            raise ValueError("Controller is not created.")

        if self.__controller.vendor == "unipi":

            self.__controller.set_webhook(self.__evok_cb)
            self.__controller.start_web_service()

            # Create entrance
            if os.name == "posix":

                # Load settings
                evok_settings = EvokSettings("/etc/evok.conf")

                # Modifie
                evok_settings.webhook_address = "http://127.0.0.1:8889/api/v1/evok/webhooks   ; Put your server endpoint address here (e.g. http://123.123.123.123:/wh )"
                evok_settings.webhook_enabled = True
                evok_settings.webhook_device_mask = ["input", "wd"]
                evok_settings.webhook_complex_events = True

                # Save
                evok_settings.save()

                # Restart the service to accept the settings.
                EvokSettings.restart()


    def __erp_set_registers(self, data):
        """ERP set registers values.

        Args:
            data (dict): Registers names and values.
        """

        # (Request to have WEB API for work with registers. MG @ 15.01.2021)


        result = {}
        registers = {}

        if data is not None:
            registers = data["registers"]

        for register_name in registers:
            register = self.__registers.by_name(register_name)
            if registers is not None:

                # Apply the changes.
                register.value = registers[register_name]

                # In th response add what is going on.
                result[register.name] = register.value
    
        return result

    def __erp_get_registers(self, data):
        """ERP get registers values.

        Args:
            registers (dict): Names of registers.

        Returns:
            dict: Dictionary of registers values and their names.
        """

        # (Request to have WEB API for work with registers. MG @ 15.01.2021)

        result = {}
        registers = {}

        if data is not None:
            registers = data["registers"]

        for register_name in registers:
            register = self.__registers.by_name(register_name)
            if register is not None:
                result[register.name] = register.value
        
        return result

    def __init_erp(self):
        """Setup the ERP.
        """

        # Take ERP info from settings.
        erp_host=self.__app_settings.get_erp_service["host"]
        erp_timeout=self.__app_settings.get_erp_service["timeout"]

        # Create ERP.
        self.__erp = bgERP(\
            host=erp_host,\
            timeout=erp_timeout)

        # Set callbacks.
        self.__erp.set_registers_cb(\
            get_cb=self.__erp_get_registers,\
            set_cb=self.__erp_set_registers)

        # Set the ERP update timer.
        self.__erp_service_update_timer = Timer(self.__erp_service_update_rate)

#endregion 

#region Private Methods Zone States

    def __cb_zone_state(self, machine):
        """Set zone state.
        """

        self.__logger.info("Zone state: {}".format(machine.get_state()))

    def __init(self):
        """Init the zone."""

        # Update the neuron.
        state = self.__controller.update()

        if state:
            # Clear all resources.
            self.__zone_state.set_state(ZoneState.Login)

        else:
            GlobalErrorHandler.log_no_connection_plc(self.__logger)

    def __login(self):
        """Login to bgERP."""

        # one_wire = self.__controller.get_1w_devices()
        # modbus = self.__controller.get_modbus_devices()
        # credentials = {
            # "one_wire=one_wire, \
            # "modbus=modbus, \
        # }

        login_state = self.__erp.login(\
            serial_number=self.__controller.serial_number,\
            model=self.__controller.model,\
            version=self.__controller.version,\
            config_time=self.__app_settings.get_erp_service["config_time"],\
            bgerp_id=self.__app_settings.get_erp_service["erp_id"])

        if login_state:
            # Rewrite the ERP service ID.
            if self.__app_settings.get_erp_service["erp_id"] != self.__erp.erp_id:
                self.__app_settings.get_erp_service["erp_id"] = self.__erp.erp_id
                self.__app_settings.save()

            self.__zone_state.set_state(ZoneState.Run)

        else:
            self.__zone_state.set_state(ZoneState.Init)

    def __run(self):

        # Update the neuron.
        state = self.__controller.update()

        if not state:
            self.__logger.error("PLC service should be restarted.")
            GlobalErrorHandler.log_no_connection_plc(self.__logger)

        # Give plugins runtime.
        self.__plugin_manager.update()

        # Update periodically bgERP.
        self.__erp_service_update_timer.update()
        if self.__erp_service_update_timer.expired:
            self.__erp_service_update_timer.clear()

            ztm_regs = self.__registers.by_scope(Scope.Device)
            ztm_regs = ztm_regs.new_then(60)
            ztm_regs_dict = ztm_regs.to_dict()

            update_state = self.__erp.sync(ztm_regs_dict)

            if update_state is not None: #  is not None
                self.__registers.update(update_state)

                # Clear the last atendies. (Eml6287)
                aa = self.__registers.by_name("ac.last_update_attendees")
                if aa is not None:
                    aa.value = str([])

                # (Eml6287)
                # (Request to stop the queue from MG @ 15.01.2021)
                # not_send_len = self.__registers_snapshot.qsize()
                # if not_send_len > 0:
                #     Get from the queue.
                #     snapshot = self.__registers_snapshot.get()
                #     Send the firs from the queue.
                #     self.__erp.sync(snapshot)

            else:

                GlobalErrorHandler.log_no_connection_erp(self.__logger)

                # # (Request to stop the queue from MG @ 15.01.2021)
                # # Create absolute copy of the object.
                # reg_copy = self.__registers.by_scope(Scope.Device).to_dict().copy()
                # # Put the copy to the queue.
                # self.__registers_snapshot.put(reg_copy)

    def __shutdown(self):
        """Shutdown procedure."""

        self.__plugin_manager.shutdown()

    def __test(self):
        """Test devices."""

        success = True

        if success:
            self.__zone_state.set_state(ZoneState.Run)

        else:
            self.__zone_state.set_state(ZoneState.Test)

#endregion

#region Private Methods Performance Profiler

    def __on_time_change(self, passed_time):

        time_usage = self.__registers.by_name("sys.time.usage")
        if time_usage is not None:
            time_usage.value = float("{:10.4f}".format(passed_time))

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

    def init(self):
        """Init the process."""

        try:
            # Application settings.
            self.__app_settings = ApplicationSettings.get_instance()

            # Create logger.
            self.__logger = get_logger(__name__)

            # Create registers.
            self.__init_registers()

            # Create PLC.
            self.__init_controller()

            # Create the plugin manager.
            self.__plugin_manager = PluginsManager(self.__registers, self.__controller)

            # Setup the ERP.
            self.__init_erp()

            # Init the runtime.
            self.__init_runtime()

            # # (Request to stop the queue from MG @ 15.01.2021)
            # self.__registers_snapshot = queue.Queue()

        except Exception:
            exc_info = sys.exc_info()
            self.__logger.error(traceback.format_exc())
            sys.exit(0)

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

        self.__zone_state.set_state(ZoneState.Shutdown)
        self.__stop_flag = True
        self.__plugin_manager.shutdown()


#endregion
