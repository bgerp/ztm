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

from enum import Enum

from plugins.base_plugin import BasePlugin

from devices.no_vendor.flowmeter import Flowmeter as FlowmeterDevice
from devices.tests.leak_test import LeakTest

from utils.timer import Timer
from utils.state_machine import StateMachine

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

class TestState(Enum):
    """Test state"""

    NONE = 0
    TekeFirstMeasurement = 1
    WaitForLeak = 2
    TekeSecondMeasurement = 3

class Flowmeter(BasePlugin):
    """Flowmeter measuring device."""

#region Variables

    __flowmetter_dev = None
    """Flow meter device."""

    __leak_test = None
    """Leak tester."""

#endregion

#region Private Methods

    def __leaktest_result(self, leak_liters):

            if leak_liters > 0:
                name = "general.drink_water_leak"
                register = self._registers.by_name(name)

                if register is not None:
                    register.value = leak_liters

#endregion

#region Public Methods

    def init(self):

        # Check timer. Every hour test.
        self.__check_timer = Timer(5) # 3600

        # Test state machine.
        self.__test_state = StateMachine(TestState.TekeFirstMeasurement)

        tpl = self._registers.by_name(self._key + ".tpl")
        input_pin = self._registers.by_name(self._key + ".input")

        if input_pin is not None and\
            tpl is not None:

            config = \
            {\
                "name": self.name,
                "input": input_pin.value,
                "tpl": tpl.value,
                "controller": self._controller
            }

            self.__flowmetter_dev = FlowmeterDevice(config)
            self.__flowmetter_dev.init()

            self.__leak_test = LeakTest(self.__flowmetter_dev)
            self.__leak_test.on_result(self.__leaktest_result)

    def update(self):
        """Update the flowmeter value."""

        fm_state = self._registers.by_name(self._key + ".state")

        if self.__flowmetter_dev is not None and\
            fm_state is not None:
            fm_state.value = self.__flowmetter_dev.get_liters()

        key = "general.is_empty"
        is_empty = self._registers.by_name(key)

        if self.__flowmetter_dev is not None and\
            is_empty is not None and\
            is_empty.value == 1:
            self.__leak_test.run()

#endregion
