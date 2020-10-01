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

from utils.logger import get_logger

from plugins.base_plugin import BasePlugin

from devices.no_vendors.no_vendor_1.flowmeter import Flowmeter
from devices.tests.leak_test.leak_test import LeakTest
from devices.Eastron.sdm120.sdm120 import SDM120
from devices.Eastron.sdm630.sdm630 import SDM630

from data import verbal_const

from services.evok.settings import EvokSettings

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

__name_space__ = "monitoring"

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

    __uart = 2
    """UART device index."""

    __dev_id = 3
    """EVOK device index."""

    __register_type = ""
    """Register type."""

    __parameters_values = []
    """Parameters values."""

    __evok_setting = None
    """EVOK settings."""

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
            register = self._registers.by_name(self._key + ".cw.leak")
            if register is not None:
                register.value = leak_liters

    def __init_cw(self):

        cw_input = self._registers.by_name(self._key + ".cw.input")
        if cw_input is not None:
            cw_input.update_handler = self.__cw_input_cb

        cw_tpl = self._registers.by_name(self._key + ".cw.tpl")
        if cw_tpl is not None:
            cw_tpl.update_handler = self.__cw_tpl_cb

        config = \
        {\
            "name": self.name + " cold water flow meter",
            "controller": self._controller
        }

        self.__cw_flowmetter_dev = Flowmeter(config)
        self.__cw_flowmetter_dev.init()

        self.__cw_leak_test = LeakTest(self.__cw_flowmetter_dev, 20)
        self.__cw_leak_test.on_result(self.__cw_leaktest_result)

    def __update_cw(self):

        fm_state = self._registers.by_name(self._key + ".cw.value")
        if self.__cw_flowmetter_dev is not None and\
            fm_state is not None:
            fm_state.value = self.__cw_flowmetter_dev.get_liters()

        # If the zone is empty check for leaks.
        is_empty = self._registers.by_name("env.is_empty")
        if self.__cw_flowmetter_dev is not None and\
            is_empty is not None and\
            is_empty.value == 1:

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
            register = self._registers.by_name(self._key + ".hw.leak")
            if register is not None:
                register.value = leak_liters

    def __init_hw(self):

        hw_input = self._registers.by_name(self._key + ".hw.input")
        if hw_input is not None:
            hw_input.update_handler = self.__hw_input_cb

        hw_tpl = self._registers.by_name(self._key + ".hw.tpl")
        if hw_tpl is not None:
            hw_tpl.update_handler = self.__hw_tpl_cb

        config = \
        {\
            "name": self.name + " hot water flow meter",
            "controller": self._controller
        }

        self.__hw_flowmetter_dev = Flowmeter(config)
        self.__hw_flowmetter_dev.init()

        self.__hw_leak_test = LeakTest(self.__hw_flowmetter_dev, 20)
        self.__hw_leak_test.on_result(self.__hw_leaktest_result)

    def __update_hw(self):

        fm_state = self._registers.by_name(self._key + ".hw.value")
        if self.__hw_flowmetter_dev is not None and\
            fm_state is not None:
            fm_state.value = self.__hw_flowmetter_dev.get_liters()

        # If the zone is empty check for leaks.
        is_empty = self._registers.by_name("env.is_empty")
        if self.__cw_flowmetter_dev is not None and\
            is_empty is not None and\
            is_empty.value == 1:

            self.__cw_leak_test.run()

#endregion

#region Private Methods (Power Analyser)

    def __pa_enabled_cb(self, register):

        if not register.data_type == "str":
            return

        if register.value != verbal_const.OFF and self.__power_analyser is None:

            # TODO: Make this action only iv EVOK is loaded.
            # Load EVOK settings.
            if os.name == "posix":
                self.__evok_setting = EvokSettings("/etc/evok.conf")
            if os.name == "nt":
                self.__evok_setting = EvokSettings("evok.conf")

            # mb-rtu/Eastron/SDM630/2/3
            # Split parammeters
            params = register.value.split("/")

            # Set device ID.
            self.__dev_id = params[4]

            # modbus type.
            if params[0] == "mb-rtu":
                self.__uart = params[3]

            # Vendor
            vendor = params[1]
            if vendor == "Eastron":

                # Model
                model = params[2]
                if model == "SDM120":
                    self.__power_analyser = SDM120()
                    self.__register_type = "inp"

                elif model == "SDM630":
                    self.__power_analyser = SDM630()
                    self.__register_type = "inp"

                if not self.__evok_setting.device_exists("EXTENTION_1"):

                    # Add extention 1.
                    extention_1 = \
                        {
                            "global_id": self.__dev_id,
                            "device_name": model,
                            "modbus_uart_port": "/dev/extcomm/0/0",
                            "allow_register_access": True,
                            "address": self.__uart,
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

            if self.__evok_setting.device_exists("EXTENTION_1"):

                # Remove the settings.
                self.__evok_setting.remove_device("EXTENTION_1")
                self.__evok_setting.save()
                self.__logger.debug("Disable the Power Analyser.")

                # Restart the service.
                if os.name == "posix":
                    EvokSettings.restart()
                    self.__logger.debug("Restart the EVOK service.")

    def __init_pa(self):

        pa_enabled = self._registers.by_name(self._key + ".pa.settings")
        if pa_enabled is not None:
            pa_enabled.update_handler = self.__pa_enabled_cb

    def __update_pa(self):

        if self.__power_analyser is None:
            return

        # Get structure data.
        registers_ids = self.__power_analyser.get_registers_ids()

        # Get values by the structure.
        registers_values = self._controller.read_mb_registers(\
            self.__uart, \
            self.__dev_id, \
            registers_ids, \
            self.__register_type)

        # Convert values to human readable.
        parameters_values = self.__power_analyser.get_parameters_values(registers_values)

        # Format the floating points.
        for parameter_value in parameters_values:
            try:
                parameters_values[parameter_value] = \
                    float("{:06.3f}".format(float(parameters_values[parameter_value])))

            except ValueError:
                parameters_values[parameter_value] = float("{:06.3f}".format(000.0))

        self.__parameters_values = parameters_values

        if  isinstance(self.__power_analyser, SDM120):

            l1_data = {\
                "Current":self.__parameters_values["Current"],\
                "ExportActiveEnergy":self.__parameters_values["ExportActiveEnergy"],\
                "ApparentPower": self.__parameters_values["ApparentPower"]\
                }

            reg_l1 = self._registers.by_name(self._key + ".pa.l1")
            if reg_l1 is not None:
                reg_l1.value = json.dumps(l1_data)

        elif  isinstance(self.__power_analyser, SDM630):

            l1_data = {\
                "Current":self.__parameters_values["Phase1Current"],\
                "ExportActiveEnergy":self.__parameters_values["L1ExportkVArh"],\
                "ApparentPower": self.__parameters_values["L1TotalkWh"]\
                }

            l2_data = {\
                "Current":self.__parameters_values["Phase2Current"],\
                "ExportActiveEnergy":self.__parameters_values["L2ExportkVArh"],\
                "ApparentPower": self.__parameters_values["L2TotalkWh"]\
                }

            l3_data = {\
                "Current":self.__parameters_values["Phase3Current"],\
                "ExportActiveEnergy":self.__parameters_values["L3ExportkVArh"],\
                "ApparentPower": self.__parameters_values["L3TotalkWh"]\
                }

            # Update parameters in the registers.
            reg_l1 = self._registers.by_name(self._key + ".pa.l1")
            if reg_l1 is not None:
                reg_l1.value = json.dumps(l1_data)

            reg_l2 = self._registers.by_name(self._key + ".pa.l2")
            if reg_l2 is not None:
                reg_l2.value = json.dumps(l2_data)

            reg_l3 = self._registers.by_name(self._key + ".pa.l3")
            if reg_l3 is not None:
                reg_l3.value = json.dumps(l3_data)

        else:
            self.__logger.error("Unknown power analyser")

#endregion

#region Public Methods

    def init(self):
        """Initialize the plugin."""

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

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

        # Update power analyser.
        self.__update_pa()

    def shutdown(self):
        """Shutting down the blinds."""

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
