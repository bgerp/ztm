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

import json
import os
import time

from utils.logger import get_logger
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin

from devices.vendors.no_vendor_1.flowmeter import Flowmeter
from devices.tests.leak_test.leak_test import LeakTest

from devices.factories.power_analyzers.power_analyser_factory import PowerAnalyserFactory

from data import verbal_const

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

__class_name__ = "Monitoring"
"""Plugin class name."""

#endregion

class Monitoring(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __cw_flowmetter_dev = None
    """Cold water flow meter."""

    __cw_leak_test = None
    """Cold water leak test."""

    __hw_flowmetter_dev = None
    """Hot water flow meter."""

    __hw_leak_test = None
    """Hot water leak test."""

    __power_analyser = None
    """Power analyser."""

    __evok_setting = None
    """EVOK settings."""

    __measurements = []
    """Power analyser measurements.
    """

    __demand_timer = None
    """Demand measuring timer.
    """

    # TODO: Add measuring timer to one hour.

#endregion
    
#region Private Methods (Cold Water Flowmeter)

    def __cw_input_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__cw_flowmetter_dev.input != register.value:
            self.__cw_flowmetter_dev.input = register.value

    def __cw_tpl_cb(self, register):

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__cw_flowmetter_dev.tpl != register.value:
            self.__cw_flowmetter_dev.tpl = register.value

    def __cw_leaktest_result(self, leak_liters):

        if leak_liters > 0:
            register = self._registers.by_name(self.key + ".cw.leak")
            if register is not None:
                register.value = leak_liters

    def __init_cw(self):

        cw_input = self._registers.by_name(self.key + ".cw.input")
        if cw_input is not None:
            cw_input.update_handlers = self.__cw_input_cb

        cw_tpl = self._registers.by_name(self.key + ".cw.tpl")
        if cw_tpl is not None:
            cw_tpl.update_handlers = self.__cw_tpl_cb

        self.__cw_flowmetter_dev = Flowmeter.create(\
            self.name + " cold water flow meter",\
            "monitoring.cw",\
            self._registers,\
            self._controller)
        self.__cw_flowmetter_dev.init()

        self.__cw_leak_test = LeakTest(self.__cw_flowmetter_dev, 20)
        self.__cw_leak_test.on_result(self.__cw_leaktest_result)

    def __update_cw(self):

        fm_state = self._registers.by_name(self.key + ".cw.value")
        if self.__cw_flowmetter_dev is not None and\
            fm_state is not None:
            fm_state.value = self.__cw_flowmetter_dev.get_liters()

        # If the zone is empty check for leaks.
        is_empty = self._registers.by_name("envm.is_empty")
        if self.__cw_flowmetter_dev is not None and\
            is_empty is not None and\
            is_empty.value:

            self.__cw_leak_test.run()

#endregion

#region Private Methods (Hot Water Flowmeter)

    def __hw_input_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__hw_flowmetter_dev.input != register.value:
            self.__hw_flowmetter_dev.input = register.value

    def __hw_tpl_cb(self, register):

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__hw_flowmetter_dev.tpl != register.value:
            self.__hw_flowmetter_dev.tpl = register.value

    def __hw_leaktest_result(self, leak_liters):

        if leak_liters > 0:
            register = self._registers.by_name(self.key + ".hw.leak")
            if register is not None:
                register.value = leak_liters

    def __init_hw(self):

        hw_input = self._registers.by_name(self.key + ".hw.input")
        if hw_input is not None:
            hw_input.update_handlers = self.__hw_input_cb

        hw_tpl = self._registers.by_name(self.key + ".hw.tpl")
        if hw_tpl is not None:
            hw_tpl.update_handlers = self.__hw_tpl_cb

        self.__hw_flowmetter_dev = Flowmeter.create(\
            self.name + " hot water flow meter",\
            "monitoring.hw",\
            self._registers,\
            self._controller)
        self.__hw_flowmetter_dev.init()

        self.__hw_leak_test = LeakTest(self.__hw_flowmetter_dev, 20)
        self.__hw_leak_test.on_result(self.__hw_leaktest_result)

    def __update_hw(self):

        fm_state = self._registers.by_name(self.key + ".hw.value")
        if self.__hw_flowmetter_dev is not None and\
            fm_state is not None:
            fm_state.value = self.__hw_flowmetter_dev.get_liters()

        # If the zone is empty check for leaks.
        is_empty = self._registers.by_name("envm.is_empty")
        if self.__hw_flowmetter_dev is not None and\
            is_empty is not None and\
            is_empty.value:

            self.__hw_leak_test.run()

#endregion

#region Private Methods (Power Analyser)

    def __read_all_parameters(self):

        black_list = [
            "GetRelays",
            "GetDigitalInputs",
            "GetAnalogOutputs",
            "GetAnalogInputs",
            "SetRelays",
            "SetAnalogOutputs",
        ]

        for parameter in self.__power_analyser.parameters:

            name = parameter.parameter_name

            if name in black_list:
                continue
            
            value = self.__read_local_parameter(name)

            print("{}: {}".format(name, value))        

    def __read_local_parameter(self, name):

        value = 0.0

        request = self.__power_analyser.generate_request(name)
        if request is not None:
            response = self._controller.execute_mb_request(request)
            if not response.isError():
                registers = {}
                for index in range(request.address, request.address + request.count):
                    registers[index] = response.registers[index - request.address]
                value = self.__power_analyser.get_parameter_value(name, registers)

        return value

    def __read_unipi_mb_master(self):

        # Get structure data.
        registers_ids = self.__power_analyser.get_registers_ids()

        # Get values by the structure.
        registers_values = self._controller.read_mb_registers(\
            self.__uart, \
            self.__dev_id, \
            registers_ids, \
            RegisterType.ReadInputRegisters)

        # Convert values to human readable.
        parameters_values = self.__power_analyser.get_parameters_values(registers_values)

        # Format the floating points.
        for parameter_value in parameters_values:
            try:
                parameters_values[parameter_value] = \
                    float("{:06.3f}".format(float(parameters_values[parameter_value])))

            except ValueError:
                parameters_values[parameter_value] = float("{:06.3f}".format(000.0))

        return parameters_values

    def __pa_enabled_cb(self, register):

        if not register.data_type == "str":
            return

        if register.value != verbal_const.OFF and self.__power_analyser is None:

            # mb-rtu/Eastron/SDM630/2/3
            # Split parammeters
            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__power_analyser = PowerAnalyserFactory.create(
                                        controller=self._controller,
                                        name="Zone Power analyser",
                                        params=params)

            if self._controller.vendor == "UniPi":

                # Load EVOK settings.
                if os.name == "posix":
                    self.__evok_setting = EvokSettings("/etc/evok.conf")
                if os.name == "nt":
                    self.__evok_setting = EvokSettings("evok.conf")

                # Save settings to the EVOK software.
                if not self.__evok_setting.device_exists("EXTENTION_1"):

                    # Vendor
                    vendor = params[0]

                    # Model
                    model = params[1]

                    # UART
                    uart = params[2]

                    # Unit
                    unit = params[3]

                    # Add extention 1.
                    extention_1 = {
                        "global_id": unit,
                        "device_name": model,
                        "modbus_uart_port": "/dev/extcomm/0/0",
                        "allow_register_access": True,
                        "address": uart,
                        "scan_frequency": 10,
                        "scan_enabled": True,
                        "baud_rate": 9600,
                        "parity": "N",
                        "stop_bits": 1
                    }

                    # Add the configuration.
                    self.__evok_setting.add_named_device(extention_1, "EXTENTION_1")
                    self.__evok_setting.save()
                    self.__logger.debug("Enable the Power Analyser.")

                    # Restart the service.
                    if os.name == "posix":
                        EvokSettings.restart()
                        self.__logger.debug("Restart the EVOK service.")

        elif register.value == verbal_const.OFF and self.__power_analyser is not None:
            self.__power_analyser = None

            if self._controller.vendor == "UniPi":

                if self.__evok_setting.device_exists("EXTENTION_1"):

                    # Remove the settings.
                    self.__evok_setting.remove_device("EXTENTION_1")
                    self.__evok_setting.save()
                    self.__logger.debug("Disable the Power Analyser.")

                    # Restart the service.
                    if os.name == "posix":
                        EvokSettings.restart()
                        self.__logger.debug("Restart the EVOK service.")

    def __pa_demand_time_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0.0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__demand_timer is not None:
            self.__demand_timer.expiration_time = register.value

    def __init_pa(self):

        pa_enabled = self._registers.by_name(self.key + ".pa.settings")
        if pa_enabled is not None:
            pa_enabled.update_handlers = self.__pa_enabled_cb
            pa_enabled.update()

        demand_time = self._registers.by_name(self.key + ".pa.demand_time")
        if demand_time is not None:
            demand_time.update_handlers = self.__pa_demand_time_cb
            demand_time.update()

    def __update_pa(self):

        if self.__power_analyser is None:
            return         

        # TODO: Ask is it necessary to have active and reactive energy.
        # self.__read_all_parameters()

        measurement = {
            "ImportActiveEnergy": 0.0,
            "ExportActiveEnergy": 0.0,
            "ImportReactiveEnergy": 0.0,
            "ExportReactiveEnergy": 0.0,
            "Phase1Current": 0.0,
            "Phase2Current": 0.0,
            "Phase3Current": 0.0,
            "ts": 0,
        }

        if self.__power_analyser.model == "SDM120":

            if self._controller.vendor == "UniPi":

                values = self.__read_unipi_mb_master()

                measurement["ImportActiveEnergy"] = values["ImportActiveEnergy"]
                measurement["ExportActiveEnergy"] = values["ExportActiveEnergy"]
                measurement["ImportReactiveEnergy"] = values["ImportReactiveEnergy"]
                measurement["ExportReactiveEnergy"] = values["ExportReactiveEnergy"]
                measurement["Phase1Current"] = values["Current"]

            else:
                measurement["ImportActiveEnergy"] = self.__read_local_parameter("ImportActiveEnergy")
                measurement["ExportActiveEnergy"] = self.__read_local_parameter("ExportActiveEnergy")
                measurement["ImportReactiveEnergy"] = self.__read_local_parameter("ImportReactiveEnergy")
                measurement["ExportReactiveEnergy"] = self.__read_local_parameter("ExportReactiveEnergy")
                measurement["Phase1Current"] = self.__read_local_parameter("Current")

        elif self.__power_analyser.model == "SDM630":

            if self._controller.vendor == "UniPi":
                values = self.__read_unipi_mb_master()
                measurement["ImportActiveEnergy"] = values["TotalImportkWh"]
                measurement["ExportActiveEnergy"] = values["TotalExportkWh"]
                measurement["ImportReactiveEnergy"] = values["TotalImportkVArh"]
                measurement["ExportReactiveEnergy"] = values["TotalExportkVArh"]
                measurement["Phase1Current"] = values["Phase1Current"]
                measurement["Phase2Current"] = values["Phase2Current"]
                measurement["Phase3Current"] = values["Phase3Current"]

            else:
                measurement["ImportActiveEnergy"] = self.__read_local_parameter("TotalImportkWh")
                measurement["ExportActiveEnergy"] = self.__read_local_parameter("TotalExportkWh")
                measurement["ImportReactiveEnergy"] = self.__read_local_parameter("TotalImportkVArh")
                measurement["ExportReactiveEnergy"] = self.__read_local_parameter("TotalExportkVArh")
                measurement["Phase1Current"] = self.__read_local_parameter("Phase1Current")
                measurement["Phase2Current"] = self.__read_local_parameter("Phase2Current")
                measurement["Phase3Current"] = self.__read_local_parameter("Phase3Current")

        else:
            self.__logger.error("Unknown power analyser")

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measuremtn to the tail.
        self.__measurements.append(measurement)

        # Update parameters in the registers.
        measurements_reg = self._registers.by_name(self.key + ".pa.measurements")
        if measurements_reg is not None:
            measurements_reg.value = json.dumps(self.__measurements)

        # TODO: The tail will become longer and longer, what to to?

#endregion

#region Public Methods

    def init(self):
        """Initialize the plugin."""

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__demand_timer = Timer(3600)

        # Init cold water flow meter.
        self.__init_cw()

        # Init hot water flow meter.
        self.__init_hw()

        # Init power analyser.
        self.__init_pa()

    def update(self):
        """Runtime of the plugin."""

        # Update cold water flow meter.
        self.__update_cw()

        # Update hot water flow meter.
        self.__update_hw()

        # Check is it time to measure.
        self.__demand_timer.update()
        if self.__demand_timer.expired:

            # Clear the timer.
            self.__demand_timer.clear()

            # Update power analyser.
            self.__update_pa()

    def shutdown(self):
        """Shutting down the blinds."""

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
