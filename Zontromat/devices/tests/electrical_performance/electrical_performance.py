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

from enum import Enum

from data.registers import Registers

from devices.HangzhouAirflowElectricApplications.f3p146ec072600.f3p146ec072600 import F3P146EC072600

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
    Init = 1
    TakeFirstConsumption = 2
    TurnTargetOn = 3
    Wait = 4
    TakeSecondConsumption = 5
    TurnTargetOff = 6
    ReturnResults = 7

class ElectricalPerformance:
    """Electrical performance test."""

#region Attributes

    __test_state = None
    """Test state machine."""

    __check_timer = None
    """Check test timer."""

    __result_cb = None
    """Callback result device."""

    __target_device = None
    """Target device."""

    __registers = None
    """Registers"""

    __consumption_1 = 0

    __consumption_2 = 0

#endregion

#region Constructor / Destructor

    def __init__(self):
        """Constructor"""

        self.__test_state = StateMachine(TestState.NONE)
        self.__check_timer = Timer(0)
        self.__registers = Registers.get_instance()

    def __del__(self):
        """Destructor"""

        if self.__check_timer is not None:
            del self.__check_timer

        if self.__test_state is not None:
            del self.__test_state

#endregion

#region Private Methods

    def __turn_target_off(self):

        if isinstance(self.__target_device, F3P146EC072600):

            self.__target_device.set_speed(0)

    def __turn_target_on(self):

        if isinstance(self.__target_device, F3P146EC072600):

            self.__target_device.set_speed(10)

    def __take_current_consumption(self):

        current_power = 0

        register = self.__registers.by_name("monitoring.pa.l1")
        if register is not None:
            register_data = json.loads(register.value)
            current_power = register_data["Current"]

        return current_power

#endregion

#region Public Methods

    def start(self):
        """Start the test."""

        self.__test_state.set_state(TestState.Init)

    def stop(self):
        """Start the test."""

        self.__turn_target_off()
        self.__test_state.set_state(TestState.NONE)

    def set_test_target(self, target_device):
        """Set test target device."""

        if target_device is None:
            return

        self.__target_device = target_device

        if isinstance(self.__target_device, F3P146EC072600):

            self.__target_device.max_speed = 10
            self.__target_device.min_speed = 0

    def on_result(self, callback):
        """On result registration."""

        if callback is None:
            return

        self.__result_cb = callback

    def run(self):
        """Run the test."""

        if self.__test_state.is_state(TestState.Init):

            self.__turn_target_off()
            self.__consumption_1 = 0
            self.__consumption_2 = 0

            self.__test_state.set_state(TestState.TakeFirstConsumption)

        elif self.__test_state.is_state(TestState.TakeFirstConsumption):

            self.__consumption_1 = self.__take_current_consumption()

            self.__test_state.set_state(TestState.TurnTargetOn)

        elif self.__test_state.is_state(TestState.TurnTargetOn):

            self.__turn_target_on()

            self.__check_timer.expiration_time = 10
            self.__check_timer.update_last_time()

            self.__test_state.set_state(TestState.Wait)

        elif self.__test_state.is_state(TestState.Wait):

            self.__check_timer.update()
            if self.__check_timer.expired:
                self.__check_timer.clear()

                self.__test_state.set_state(TestState.TakeSecondConsumption)

        elif self.__test_state.is_state(TestState.TakeSecondConsumption):

            self.__consumption_1 = self.__take_current_consumption()

            self.__test_state.set_state(TestState.TurnTargetOff)

        elif self.__test_state.is_state(TestState.TurnTargetOff):

            self.__turn_target_off()

            self.__test_state.set_state(TestState.ReturnResults)

        elif self.__test_state.is_state(TestState.ReturnResults):

            consuption_w = self.__consumption_2 - self.__consumption_1

            if self.__result_cb is not None:
                self.__result_cb(consuption_w)

            self.__test_state.set_state(TestState.NONE)

#endregion
