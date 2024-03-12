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
import time
import traceback
import os

from utils.settings import ApplicationSettings
from utils.logger import get_logger, crate_log_file
from utils.performance_profiler import PerformanceProfiler
from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer
from utils.updater import update as software_update
from utils.utils import uptime

from controllers.controller_factory import ControllerFactory

from bg_erp.bg_erp import bgERP
from bg_erp.erp_state import ERPState

from data.register import Scope
from data.registers import Registers
from data.registers import Register

from plugins.plugins_manager import PluginsManager

from services.evok.settings import EvokSettings
from services.global_error_handler.global_error_handler import GlobalErrorHandler

from ztm_ui.ztm_ui import ZtmUI

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

class Zone():
    """Main zone class"""

#region Attributes

    __performance_profiler = PerformanceProfiler()
    """Performance profiler.
    """

#endregion

#region Constructor

    def __init__(self):
        self.__logger = None
        """Logger"""

        self.__app_settings = None
        """Application settings."""

        self.__controller = None
        """Neuron controller."""

        self.__erp = None
        """Communication with the ERP."""

        self.__registers = None
        """Registers"""

        self.__plugin_manager = None
        """Plugin manager."""

        self.__update_rate = 0.5
        """Controlling update rate in seconds."""

        self.__update_timer = None
        """Update timer."""

        self.__erp_service_update_timer = None
        """ERP update timer."""

        self.__erp_state_machine = None
        """Zone state."""

        self.__stop_flag = False
        """Time to Stop flag."""

        self.__busy_flag = False
        """Busy flag."""

        self.__performance_profiler_timer = None
        """Performance profiler timer."""

        # (Request to stop the queue from MG @ 15.01.2021)
        # __registers_snapshot = None
        # """Registers snapshot."""

        self.__ztm_ui = None
        """Zontromat UI
        """

        self.__ztm_ui_temp_data = None
        """UI data
        """

        self.__ztm_ui_ut = None
        """ZtmUI update timer.
        """
        self.__ztm_ui_weather_cast_ut = None
        """ZtmUI update timer.
        """
        self.__ztm_ui_heartbeat_ut = None
        """ZtmUI update timer.
        """

#endregion

#region Private Methods (Registers Interface)

    def __target_version_cb(self, register: Register):

        current_version = None
        target_version = None

        target_version_reg = register

        # Check data type of the current version.
        if not target_version_reg.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, target_version_reg)
            return

        # Get target version value.
        if target_version_reg.value is not None:
            target_version = target_version_reg.value

        # Check the target version value.
        if target_version == None:
            GlobalErrorHandler.log_bad_register_value(self.__logger, target_version)
            return

        # Get current version register.
        current_version_reg = self.__registers.by_name("sys.software.current_version")

        # Check data type.
        if not ((current_version_reg.data_type == "json")):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, current_version_reg)
            return

        if current_version_reg is not None:
            current_version = current_version_reg.value

        # Check the current version value.
        if current_version == None:
            GlobalErrorHandler.log_bad_register_value(self.__logger, current_version)
            return

        # Update the software.
        software_update(current_version_reg.value, target_version_reg.value)

        # Save the current version.
        self.__app_settings.current_version = target_version_reg.value
        self.__app_settings.save()

    def __init_registers(self):
        """Setup registers source.
        """

        registers_file = ""

        # Current file path. & Go to file.
        cwf = os.path.dirname(os.path.abspath(__file__))
        registers_file = os.path.join(cwf, "..", "registers.json")

        # Load depending of file format.
        if registers_file.endswith('json'):
            self.__registers = Registers.from_json(registers_file)
        elif registers_file.endswith('csv'):
            self.__registers = Registers.from_csv(registers_file)
        else:
            sys.exit(0)

        target_version = self.__registers.by_name("sys.software.current_version")
        if target_version is not None:
            target_version.value = self.__app_settings.current_version

        target_version = self.__registers.by_name("sys.software.target_version")
        if target_version is not None:
            target_version.update_handlers = self.__target_version_cb
            # TODO: Will we ask for update on every start?

        # Set boot time.
        sys_boot_time = self.__registers.by_name("sys.time.boot")
        if sys_boot_time is not None:
            sys_boot_time.value = time.time() - uptime()

        # Set startup time.
        sys_startup_time = self.__registers.by_name("sys.time.startup")
        if sys_startup_time is not None:
            sys_startup_time.value = time.time()

#endregion

#region Private Methods (PLC)

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

                    if self.__registers is not None:
                        self.__registers.write(required_name, device["value"])

    def __init_controller(self):
        """Initialize the controller.
        """

        # Create PLC.
        self.__controller = ControllerFactory.create(self.__app_settings.controller)

        if self.__controller is None:
            raise ValueError("Controller is not created.")

        # Print out the vendor and model of the controller.
        self.__logger.info(self.__controller)

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

#endregion

#region Private Methods (ERP)

    def __on_erp_state_change_cb(self, machine):
        """React on ERP state changes.

        Args:
            machine (StateMachine): State machine state.
        """

        self.__logger.info("ERP state: {}".format(machine.get_state()))

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
        erp_host = self.__app_settings.erp_service["host"]
        erp_timeout = self.__app_settings.erp_service["timeout"]

        # Create ERP.
        self.__erp = bgERP(host=erp_host, timeout=erp_timeout)

        # Set callbacks.
        self.__erp.set_registers_cb(
            get_cb=self.__erp_get_registers,
            set_cb=self.__erp_set_registers)

        # (Eml9649)
        # Set the ERP update timer.
        self.__erp_service_update_timer = Timer(
            int(self.__app_settings.erp_service["update_rate"]) +
                # Add phase shift time for reducing the self DDoS attack to the server.
                int(self.__app_settings.erp_service["serial_number"]) * 0.5)

        # Set zone state machine.
        self.__erp_state_machine = StateMachine()
        self.__erp_state_machine.on_change(self.__on_erp_state_change_cb)
        self.__erp_state_machine.set_state(ERPState.NONE)

    def __erp_login(self):
        """Login to bgERP.
        """

        login_state = self.__erp.login(
            serial_number=self.__controller.serial_number,
            model=self.__controller.model,
            version=self.__controller.version,
            config_time=self.__app_settings.erp_service["config_time"],
            bgerp_id=self.__app_settings.erp_service["erp_id"])

        if login_state:
            # Rewrite the ERP service ID.
            if self.__app_settings.erp_service["erp_id"] != self.__erp.erp_id:
                self.__app_settings.erp_service["erp_id"] = self.__erp.erp_id
                self.__app_settings.save()

            self.__erp_state_machine.set_state(ERPState.Update)

        else:
            self.__erp_state_machine.set_state(ERPState.Login)

    def __erp_update(self):
        """Sync registers.
        """

        # Update periodically bgERP.
        self.__erp_service_update_timer.update()
        if self.__erp_service_update_timer.expired:
            self.__erp_service_update_timer.clear()

            # (Eml9649)
            # This check does it pass first time.
            # This will coss a initial delay that will allow to phase shift by the time of 0.5 seconds,
            # to reduce chance of  self DDoS attack.
            if self.__erp_service_update_timer.expiration_time != \
                int(self.__app_settings.erp_service["update_rate"]):
                # After first pass.
                # change the time to the standard update time and it will
                #  do the same intervals again as required.
                self.__erp_service_update_timer.expiration_time = \
                int(self.__app_settings.erp_service["update_rate"])

            ztm_regs = self.__registers.by_scope(Scope.Device)
            ztm_regs = ztm_regs.new_then(60)
            ztm_regs_dict = ztm_regs.to_dict()

            update_state = self.__erp.sync(ztm_regs_dict)

            if update_state is not None: #  is not None

                if self.__registers is not None:
                    self.__registers.update(update_state)
                    # Clear the last attendees. (Eml6287)
                    self.__registers.write("ac.last_update_attendees", str([]))

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
                self.__erp_state_machine.set_state(ERPState.Login)
                # # (Request to stop the queue from MG @ 15.01.2021)
                # # Create absolute copy of the object.
                # reg_copy = self.__registers.by_scope(Scope.Device).to_dict().copy()
                # # Put the copy to the queue.
                # self.__registers_snapshot.put(reg_copy)

    def __update_erp(self):
        """Update ERP.
        """

        if self.__erp_state_machine.is_state(ERPState.Login):
            # Login room.
            self.__erp_login()

        elif self.__erp_state_machine.is_state(ERPState.Update):
            # Run the process of the room.
            self.__erp_update()

        elif self.__erp_state_machine.is_state(ERPState.NONE):
            self.__erp_state_machine.set_state(ERPState.Login)

#endregion

#region Private Methods (ZtmUI)

    def __init_ztmui(self):

        # Check is it enabled.
        if self.__app_settings.ui["enabled"] == "True":

            self.__ztm_ui = ZtmUI(host = self.__app_settings.ui["host"],
                email = self.__app_settings.ui["email"],
                password = self.__app_settings.ui["password"],
                timeout = self.__app_settings.ui["timeout"])

            self.__ztm_ui_ut = Timer(1)
            self.__ztm_ui_weather_cast_ut = Timer(600)
            self.__ztm_ui_heartbeat_ut = Timer(3600)

            # Log in.
            if not self.__ztm_ui.is_logged_in():
                self.__ztm_ui.login()


    def __update_weather_cast(self):
        # print("Time to update")

        target_regs_names = ["envm.forecast.icon_0", "envm.forecast.rh_0", "envm.forecast.temp_0", "envm.forecast.wind_0",
                        "envm.forecast.icon_3", "envm.forecast.rh_3", "envm.forecast.temp_3", "envm.forecast.wind_3",
                        "envm.forecast.icon_6", "envm.forecast.rh_6", "envm.forecast.temp_6", "envm.forecast.wind_6"]
        target_regs_values = []

        target_regs_ztmui = []

        for target_name in target_regs_names:
            register = self.__registers.by_name(target_name)
            if register is not None:
                target_regs_values.append(register)

        for target_value in target_regs_values:
            name = target_value.name
            value = target_value.value
            minimum = 0
            maximum = 0
            status = "Normal" # enum('Rising', 'Falling', 'Normal')
            reg = {"name": name, "value": value, "min": minimum, "max": maximum, "status": status}
            target_regs_ztmui.append(reg)

        # for item in target_regs_ztmui:
        #     print(item)

        if target_regs_ztmui != []:
            # print("OK pass the updates")
            self.__ztm_ui.set(target_regs_ztmui)

    def __transport_registers_ztmui(self):
        # Check UI data and send only if changes ocurred.
        registers_ui = self.__ztm_ui.get()
        if registers_ui != []:
            if self.__ztm_ui_temp_data != registers_ui:
                self.__ztm_ui_temp_data = registers_ui
                # Update changes.
                for register in registers_ui:
                    try:
                        target_register = self.__registers.by_name(register["name"])
                        if target_register is not None:
                            if target_register.data_type == "float":
                                target_register.value = float(register["value"])
                            elif target_register.data_type == "int":
                                target_register.value = float(register["value"])
                    except Exception as e:
                        self.__logger.error(e)

    def __update_min_max(self, register):

        target_register = self.__registers.by_name(register["name"])
        if target_register is not None:
            print(target_register.name)
            print()

    def __update_ztmui(self):

        # Check is it enabled.
        if self.__app_settings.ui["enabled"] == "True":

            # self.__update_min_max(register)

            # Get periodically slider data.
            self.__ztm_ui_ut.update()
            if self.__ztm_ui_ut.expired:
                self.__ztm_ui_ut.clear()
                # Check is it logged in.
                if self.__ztm_ui.is_logged_in():
                    self.__transport_registers_ztmui()
                # If not, login.
                else:
                    self.__ztm_ui.login()

            # Update periodically weather cast data.
            self.__ztm_ui_weather_cast_ut.update()
            if self.__ztm_ui_weather_cast_ut.expired:
                self.__ztm_ui_weather_cast_ut.clear()
                # Check is it logged in.
                if self.__ztm_ui.is_logged_in():
                    if self.__erp.is_logged():
                        # Update Weather.
                        self.__update_weather_cast()
                # If not, login.
                else:
                    self.__ztm_ui.login()

            # Update periodically bgERP.
            self.__ztm_ui_heartbeat_ut.update()
            if self.__ztm_ui_heartbeat_ut.expired:
                self.__ztm_ui_heartbeat_ut.clear()
                # Check is it logged in.
                if self.__ztm_ui.is_logged_in():
                    # Send heartbeat.
                    self.__ztm_ui.heart_beat()
                # If not, login.
                else:
                    self.__ztm_ui.login()

#endregion

#region Private Methods (Runtime)

    def __init_runtime(self):

        # Update timer.
        self.__update_timer = Timer(self.__update_rate)

        # Update with offset based on the serial number of the device.
        time_offset = 0
        if self.__controller.serial_number is not None and self.__controller.serial_number.isdigit():
            time_offset = int(self.__controller.serial_number)

        # Preset the time.
        self.__update_timer.expiration_time += (time_offset / 1000)

#endregion

#region Private Methods (Performance Profiler)

    def __init_performance_profiler(self):
        """Set the performance profiler.
        """

        self.__performance_profiler.enable_mem_profile = True
        self.__performance_profiler.enable_time_profile = True
        self.__performance_profiler.on_time_change(self.__on_time_change)
        self.__performance_profiler.on_memory_change(self.__on_memory_change)

        # Setup the performance profiler timer. (60) 10 is for tests.
        self.__performance_profiler_timer = Timer(10)

    def __on_time_change(self, passed_time):
        """On consumed time change.

        Args:
            passed_time (int): Consumed runtime.
        """

        if self.__registers is not None:

            self.__registers.write("sys.time.usage", float("{:10.3f}".format(passed_time)))

    def __on_memory_change(self, current, peak):
        """On RAM memory change.

        Args:
            current (int): Current RAM.
            peak (int): Peak RAM.
        """

        if self.__registers is not None:

            self.__registers.write("sys.ram.current", float("{:10.4f}".format(current)))
            self.__registers.write("sys.ram.peak", float("{:10.4f}".format(peak)))

        # print(f"Current memory usage is {current / 10**3}kB; Peak was {peak / 10**3}kB")

    @__performance_profiler.profile
    def __update(self):
        """Update the zone.
        """

        # Create log if if it does not.
        crate_log_file()

        # Update Zontromat UI.
        self.__update_ztmui()

        # Update the neuron.
        state = self.__controller.update()
        if not state:
            self.__logger.error("PLC service should be restarted.")
            GlobalErrorHandler.log_no_connection_plc(self.__logger)
            return

        # Give plugins runtime.
        self.__plugin_manager.update()

        self.__update_erp()

        # Update uptime.
        sys_uptime_time = self.__registers.by_name("sys.time.uptime")
        if sys_uptime_time is not None:
            sys_uptime_time.value = uptime()

#endregion

#region Public Methods

    def init(self):
        """Initialize the process.
        """

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

            # Setup the ZtmUI
            self.__init_ztmui()

            # Initialize the performance profiler.
            self.__init_performance_profiler()

            # Initialize the runtime.
            self.__init_runtime()

            # # (Request to stop the queue from MG @ 15.01.2021)
            # self.__registers_snapshot = queue.Queue()

        except Exception:
            self.__logger.error(traceback.format_exc())
            sys.exit(0)

    def run(self):
        """Run the zone.
        """

        self.__logger.info("Starting up the Zone")

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

                self.__busy_flag = False

        # Wait until the main teared ends.
        while self.__busy_flag == True:
            pass

        self.__logger.info("Shutting down the Zone")

        # Shutdown the plugins.
        self.__plugin_manager.shutdown()

    def shutdown(self):
        """Shutdown the process.
        """

        self.__stop_flag = True

#endregion
