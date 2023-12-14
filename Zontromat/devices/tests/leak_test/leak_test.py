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

from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer

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

class TestState(Enum):
    """Test state"""

    NONE = 0
    TakeFirstMeasurement = 1
    TurnOffPeripheral = 2
    WaitForLeak = 3
    TakeSecondMeasurement = 4

class LeakTest:
    """Leak test class."""

#region Attributes

    __test_state = None
    """Test state machine."""

    __check_timer = None
    """Leak test timer."""

    __flowmeter_dev = None
    """Flow meter device."""

    __result_cb = None
    """Callback result device."""

    __first_measurement = 0
    """First measurement of loop flow meter."""

    __second_measurement = 0
    """Second measurement of loop flow meter."""

#endregion

#region Constructor / Destructor

    def __init__(self, flowmeter, test_time):
        self.__flowmeter_dev = flowmeter
        self.__test_state = StateMachine(TestState.TakeFirstMeasurement)
        self.__check_timer = Timer(test_time)

    def __del__(self):

        if self.__check_timer is not None:
            del self.__check_timer

        if self.__test_state is not None:
            del self.__test_state

#endregion

#region Public Methods

    def on_result(self, callback):
        """On result registration."""

        if callback is None:
            return

        self.__result_cb = callback

    def run(self):
        """Run the test."""

        self.__check_timer.update()
        if self.__check_timer.expired:
            self.__check_timer.clear()

            if self.__test_state.is_state(TestState.WaitForLeak):
                if self.__test_state.was(TestState.TakeFirstMeasurement):
                    self.__test_state.set_state(TestState.TakeSecondMeasurement)

                elif self.__test_state.was(TestState.TakeSecondMeasurement):
                    self.__test_state.set_state(TestState.TakeFirstMeasurement)

            elif self.__test_state.is_state(TestState.TakeFirstMeasurement):
                if self.__flowmeter_dev != None:
                    self.__first_measurement = self.__flowmeter_dev.get_liters()
                    if self.__first_measurement != None:
                        self.__test_state.set_state(TestState.WaitForLeak)

            elif self.__test_state.is_state(TestState.TakeSecondMeasurement):
                if self.__flowmeter_dev != None:
                    self.__second_measurement = self.__flowmeter_dev.get_liters()
                    if self.__second_measurement != None:
                        self.__test_state.set_state(TestState.WaitForLeak)

            if self.__first_measurement != None and self.__second_measurement != None:
                leak_liters = abs(self.__second_measurement - self.__first_measurement)

                if self.__result_cb is not None:
                    self.__result_cb(leak_liters)

#endregion
