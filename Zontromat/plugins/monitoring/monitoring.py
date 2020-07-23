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

import os
import json

from utils.logger import get_logger
from utils.timer import Timer

from plugins.base_plugin import BasePlugin
from plugins.monitoring.monitoring_level import MonitoringLevel
from plugins.monitoring.rule import Rule
from plugins.monitoring.rules import Rules

from devices.no_vendor.flowmeter import Flowmeter
from devices.tests.leak_test.leak_test import LeakTest
from devices.Eastron.sdm120 import SDM120
from devices.Eastron.sdm630 import SDM630

from data import verbal_const

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

    __update_timer = None
    """Update timer."""

    __rules = None
    """Rules"""

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

#endregion

#region Private Methods (Colision Detection)

    def __setup_rules(self):

        self.__rules = Rules()

        # GPIOs
        for index in range(9):
            self.__rules.add(Rule("DO{}".format(index), MonitoringLevel.Error))
            self.__rules.add(Rule("DI{}".format(index), MonitoringLevel.Warning))
            self.__rules.add(Rule("AO{}".format(index), MonitoringLevel.Error))
            self.__rules.add(Rule("AI{}".format(index), MonitoringLevel.Warning))
            self.__rules.add(Rule("RO{}".format(index), MonitoringLevel.Error))

        # 1 Wire devices
        ow_devices = self._controller.get_1w_devices()
        for ow_device in ow_devices:
            self.__rules.add(Rule(ow_device["circuit"], MonitoringLevel.Info))

        # Serial Ports
        if os.name == "nt":
            self.__rules.add(Rule("COM4", MonitoringLevel.Error))
            self.__rules.add(Rule("COM5", MonitoringLevel.Error))

        elif os.name == "posix":
            self.__rules.add(Rule("/dev/ttyUSB0", MonitoringLevel.Error))
            self.__rules.add(Rule("/dev/ttyUSB1", MonitoringLevel.Error))

        # Add event.
        self.__rules.on_event(self.__on_event)

    def __on_event(self, intersections, rule: Rule):
        """On event callback for collisions."""

        level = MonitoringLevel(rule.level)

        if level == MonitoringLevel.Debug:
            self.__logger.debug("Debug")
            self.__logger.debug(intersections)

        if level == MonitoringLevel.Info:
            # self.__logger.info("Info")
            # self.__logger.info(intersections)

            info_message = self._registers.by_name(self._key + ".info_message")
            if info_message is not None:
                info_message.value = str(intersections)

        if level == MonitoringLevel.Warning:
            # self.__logger.warning("Warning")
            # self.__logger.warning(intersections)

            warning_message = self._registers.by_name(self._key + ".warning_message")
            if warning_message is not None:
                warning_message.value = str(intersections)

        if level == MonitoringLevel.Error:
            # self.__logger.error("Error")
            # self.__logger.error(intersections)

            error_message = self._registers.by_name(self._key + ".error_message")
            if error_message is not None:
                error_message.value = str(intersections)

    def __clear_errors_cb(self, register):
        """Clear errors callback."""

        if register.value == 1:
            # Clear the flag.
            register.value = 0

            # Clear info messages.
            info_message = self._registers.by_name(self._key + ".info_message")
            if info_message is not None:
                info_message.value = ""

            # Clear warning messages.
            warning_message = self._registers.by_name(self._key + ".warning_message")
            if warning_message is not None:
                warning_message.value = ""

            # Clear error messages.
            error_message = self._registers.by_name(self._key + ".error_message")
            if error_message is not None:
                error_message.value = ""

#endregion

#region Private Methods (Cold Water Flowmeter)

    def __cw_input_cb(self, register):

        self.__cw_flowmetter_dev.input = register.value

    def __cw_tpl_cb(self, register):

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

        self.__hw_flowmetter_dev.input = register.value

    def __hw_tpl_cb(self, register):

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

    def __uart_cb(self, register):

        self.__uart = register.value

    def __dev_id_cb(self, register):

        self.__dev_id = register.value

    def __init_pa(self):

        uart = self._registers.by_name(self._key + ".pa.uart")
        if uart is not None:
            uart.update_handler = self.__uart_cb

        dev_id = self._registers.by_name(self._key + ".pa.dev_id")
        if dev_id is not None:
            dev_id.update_handler = self.__dev_id_cb

        vendor = self._registers.by_name(self._key + ".pa.vendor").value
        if vendor == "Eastron":

            model = self._registers.by_name(self._key + ".pa.model").value
            if model == "SDM120":
                self.__power_analyser = SDM120()
                self.__register_type = "inp"

            elif model == "SDM630":
                self.__power_analyser = SDM630()
                self.__register_type = "inp"

    def __update_pa(self):

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
                    float('{:06.3f}'.format(float(parameters_values[parameter_value])))

            except ValueError:
                parameters_values[parameter_value] = float('{:06.3f}'.format(000.0))

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

        self.__update_timer = Timer(1)

        self.__setup_rules()

        clear_errors = self._registers.by_name(self._key + ".clear_errors")
        if clear_errors is not None:
            clear_errors.update_handler = self.__clear_errors_cb
            clear_errors.value = 1

        # Init cold water flow meter.
        self.__init_cw()

        # Init hot water flow meter.
        self.__init_hw()

        # Init power analyser.
        self.__init_pa()

    def update(self):
        """Runtime of the plugin."""

        # Update the timer.
        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            self.__rules.check(self._registers.to_dict())

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
