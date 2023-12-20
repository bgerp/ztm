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
from utils.logic.functions import filter_measurements_by_time

from plugins.base_plugin import BasePlugin

from devices.tests.leak_test.leak_test import LeakTest
from devices.factories.power_analyzers.power_analyser_factory import PowerAnalyzerFactory
from devices.factories.flowmeters.flowmeters_factory import FlowmeterFactory
from devices.drivers.modbus.function_code import FunctionCode

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
    """Logger
    """

    __cw_flowmeter_dev = None
    """Cold water flow meter.
    """

    __cw_leak_test = None
    """Cold water leak test.
    """

    __cw_measurements = []
    """How water measurements.
    """

    __hw_flowmeter_dev = None
    """Hot water flow meter.
    """

    __hw_leak_test = None
    """Hot water leak test.
    """

    __hw_measurements = []
    """How water measurements.
    """

    __power_analyzer = None
    """Power analyzer.
    """

    __evok_setting = None
    """EVOK settings.
    """

    __pa_measurements = []
    """Power analyzer measurements.
    """

    __demand_timer = None
    """Demand measuring timer.
    """

#endregion

#region Private Methods

#endregion

#region Private Methods (Cold Water Flowmeter)

    def __cw_flowmeter_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cw_flowmeter_dev is None:
            self.__cw_flowmeter_dev = FlowmeterFactory.create(
                name="Cold water flowmeter",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cw_flowmeter_dev is not None:
                self.__cw_flowmeter_dev.init()

                # 20 seconds is time for leak testing.
                self.__cw_leak_test = LeakTest(self.__cw_flowmeter_dev, 20)
                self.__cw_leak_test.on_result(self.__cw_leaktest_result)

        elif register.value != {} and self.__cw_flowmeter_dev is not None:
            self.__cw_flowmeter_dev.shutdown()
            del self.__cw_flowmeter_dev
            del self.__cw_leak_test
            self.__cw_flowmeter_dev = FlowmeterFactory.create(
                name="Cold water flowmeter",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cw_flowmeter_dev is not None:
                self.__cw_flowmeter_dev.init()

                # 20 seconds is time for leak testing.
                self.__cw_leak_test = LeakTest(self.__cw_flowmeter_dev, 20)
                self.__cw_leak_test.on_result(self.__cw_leaktest_result)

        elif register.value == {} and self.__cw_flowmeter_dev is not None:
            self.__cw_flowmeter_dev.shutdown()
            del self.__cw_flowmeter_dev
            del self.__cw_leak_test

    def __cw_leaktest_result(self, leak_liters):

        if leak_liters > 0:
            self._registers.write("{}.cw.leak".format(self.key), leak_liters)

    def __init_cw(self):

        cw_flowmeter = self._registers.by_name("{}.cw.flowmeter_settings".format(self.key))
        if cw_flowmeter is not None:
            cw_flowmeter.update_handlers = self.__cw_flowmeter_settings_cb
            cw_flowmeter.update()

    def __update_cw(self):

        if self.__cw_flowmeter_dev is None:
            return

        measurement = {
            "CumulativeTraffic": 0.0,
            "InstantaneousFlow": 0.0,
            "WaterTemperature" : 0.0,
            "BatteryVoltage" : 0.0,
            "ts": 0,
        }

        if self.__cw_flowmeter_dev.model == "MW-UML-15":
            if self._controller.vendor == "UniPi":
                values = self.__read_unipi_mb_master()
                for item in measurement:
                    measurement[item] = values[item]

            else:
                for item in measurement:
                    if item == "ts":
                        pass
                    measurement[item] = self.__cw_flowmeter_dev.get_value(item)

        else:
            self.__logger.error("Unknown power water meter")

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__cw_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__cw_measurements, 86400)

        # Update parameters in the registers.
        self._registers.write("{}.cw.measurements".format(self.key), json.dumps(self.__cw_measurements))

        print(f"{self.__cw_flowmeter_dev}")
        print(f"CW: {self.__cw_measurements}")

        # If the zone is empty check for leaks.
        is_empty = self._registers.by_name("envm.is_empty")
        if self.__cw_flowmeter_dev is not None and\
            is_empty is not None and\
            is_empty.value:

            self.__cw_leak_test.run()

#endregion

#region Private Methods (Hot Water Flowmeter)

    def __hw_flowmeter_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__hw_flowmeter_dev is None:
            self.__hw_flowmeter_dev = FlowmeterFactory.create(
                name="Hot water flowmeter",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__hw_flowmeter_dev is not None:
                self.__hw_flowmeter_dev.init()

                # 20 seconds is time for leak testing.
                self.__hw_leak_test = LeakTest(self.__hw_flowmeter_dev, 20)
                self.__hw_leak_test.on_result(self.__hw_leaktest_result)

        elif register.value != {} and self.__hw_flowmeter_dev is not None:
            self.__hw_flowmeter_dev.shutdown()
            del self.__hw_flowmeter_dev
            del self.__hw_leak_test
            self.__hw_flowmeter_dev = FlowmeterFactory.create(
                name="Cold water flowmeter",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__hw_flowmeter_dev is not None:
                self.__hw_flowmeter_dev.init()

                # 20 seconds is time for leak testing.
                self.__hw_leak_test = LeakTest(self.__hw_flowmeter_dev, 20)
                self.__hw_leak_test.on_result(self.__hw_leaktest_result)

        elif register.value == {} and self.__hw_flowmeter_dev is not None:
            self.__hw_flowmeter_dev.shutdown()
            del self.__hw_flowmeter_dev
            del self.__hw_leak_test

    def __hw_leaktest_result(self, leak_liters):

        if leak_liters > 0:
            self._registers.write("{}.hw.leak".format(self.key), leak_liters)

    def __init_hw(self):

        hw_flowmeter = self._registers.by_name("{}.hw.flowmeter_settings".format(self.key))
        if hw_flowmeter is not None:
            hw_flowmeter.update_handlers = self.__hw_flowmeter_settings_cb
            hw_flowmeter.update()

    def __update_hw(self):

        if self.__hw_flowmeter_dev is None:
            return

        measurement = {
            "CumulativeTraffic": 0.0,
            "InstantaneousFlow": 0.0,
            "WaterTemperature" : 0.0,
            "BatteryVoltage" : 0.0,
            "ts": 0,
        }

        if self.__hw_flowmeter_dev.model == "MW-UML-15":
            if self._controller.vendor == "UniPi":
                values = self.__read_unipi_mb_master()
                for item in measurement:
                    measurement[item] = values[item]

            else:
                for item in measurement:
                    if item == "ts":
                        pass
                    measurement[item] = self.__hw_flowmeter_dev.get_value(item)

        else:
            self.__logger.error("Unknown power water meter")

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__hw_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__hw_measurements, 86400)

        # Update parameters in the registers.
        self._registers.write("{}.hw.measurements".format(self.key), json.dumps(self.__hw_measurements))

        # If the zone is empty check for leaks.
        is_empty = self._registers.by_name("envm.is_empty")
        if self.__hw_flowmeter_dev is not None and\
            is_empty is not None and\
            is_empty.value:

            self.__hw_leak_test.run()

#endregion

#region Private Methods (Power Analyzer)

    def __read_unipi_mb_master(self):

        # Get structure data.
        registers_ids = self.__power_analyzer.get_registers_ids()

        # Get values by the structure.
        registers_values = self._controller.read_mb_registers(\
            self.__uart, \
            self.__dev_id, \
            registers_ids, \
            FunctionCode.ReadInputRegisters)

        # Convert values to human readable.
        parameters_values = self.__power_analyzer.get_parameters_values(registers_values)

        # Format the floating points.
        for parameter_value in parameters_values:
            try:
                parameters_values[parameter_value] = \
                    float("{:06.3f}".format(float(parameters_values[parameter_value])))

            except ValueError:
                parameters_values[parameter_value] = float("{:06.3f}".format(000.0))

        return parameters_values

    def __pa_enabled_cb(self, register):

        if not register.data_type == "json":
            return

        if register.value != {} and self.__power_analyzer is None:

            self.__power_analyzer = PowerAnalyzerFactory.create(
                controller=self._controller,
                name="Zone Power analyser",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self._controller.vendor == "UniPi":

                # Load EVOK settings.
                if os.name == "posix":
                    self.__evok_setting = EvokSettings("/etc/evok.conf")
                if os.name == "nt":
                    self.__evok_setting = EvokSettings("evok.conf")

                # Save settings to the EVOK software.
                if not self.__evok_setting.device_exists("EXTENTION_1"):

                    # Vendor
                    # vendor = register.value['vendor']

                    # Model
                    model = register.value['model']

                    # UART
                    uart = register.value['model']

                    # Unit
                    unit = register.value['options']['unit']

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

        elif register.value == {} and self.__power_analyzer is not None:
            self.__power_analyzer = None

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

        # if self.__demand_timer is not None:
        #     self.__demand_timer.expiration_time = register.value

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

        if self.__power_analyzer is None:
            return

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

        if self.__power_analyzer.model == "SDM120":

            if self._controller.vendor == "UniPi":

                values = self.__read_unipi_mb_master()

                measurement["ImportActiveEnergy"] = values["ImportActiveEnergy"]
                measurement["ExportActiveEnergy"] = values["ExportActiveEnergy"]
                measurement["ImportReactiveEnergy"] = values["ImportReactiveEnergy"]
                measurement["ExportReactiveEnergy"] = values["ExportReactiveEnergy"]
                measurement["Phase1Current"] = values["Current"]

            else:
                measurement["ImportActiveEnergy"] = self.__power_analyzer.get_value("ImportActiveEnergy")
                measurement["ExportActiveEnergy"] = self.__power_analyzer.get_value("ExportActiveEnergy")
                measurement["ImportReactiveEnergy"] = self.__power_analyzer.get_value("ImportReactiveEnergy")
                measurement["ExportReactiveEnergy"] = self.__power_analyzer.get_value("ExportReactiveEnergy")
                measurement["Phase1Current"] = self.__power_analyzer.get_value("Current")

        elif self.__power_analyzer.model == "SDM630":

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
                measurement["ImportActiveEnergy"] = self.__power_analyzer.get_value("TotalImportkWh")
                measurement["ExportActiveEnergy"] = self.__power_analyzer.get_value("TotalExportkWh")
                measurement["ImportReactiveEnergy"] = self.__power_analyzer.get_value("TotalImportkVArh")
                measurement["ExportReactiveEnergy"] = self.__power_analyzer.get_value("TotalExportkVArh")
                measurement["Phase1Current"] = self.__power_analyzer.get_value("Phase1Current")
                measurement["Phase2Current"] = self.__power_analyzer.get_value("Phase2Current")
                measurement["Phase3Current"] = self.__power_analyzer.get_value("Phase3Current")

        else:
            self.__logger.error("Unknown power analyser")

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__pa_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__pa_measurements, 86400)

        # Update parameters in the registers.
        self._registers.write("{}.pa.measurements".format(self.key), json.dumps(self.__pa_measurements))

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__demand_timer = Timer(5) # 3600

        # Init cold water flow meter.
        self.__init_cw()

        # Init hot water flow meter.
        self.__init_hw()

        # Init power analyzer.
        self.__init_pa()

    def _update(self):
        """Update the plugin.
        """

        # Check is it time to measure.
        self.__demand_timer.update()
        if self.__demand_timer.expired:

            # Clear the timer.
            self.__demand_timer.clear()

            # Update cold water flow meter.
            self.__update_cw()

            # Update hot water flow meter.
            self.__update_hw()

            # Update power analyzer.
            self.__update_pa()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
