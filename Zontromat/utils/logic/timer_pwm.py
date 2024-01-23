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

import time

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

from enum import Enum
from .timer import Timer

class TimerPWMState(Enum):
    """Timer PWM states.
    """

    LOWER_LIMIT = 1
    TIME_TO_ON = 2
    TIME_TO_OFF = 3
    UPPER_LIMIT = 4

class TimerPWM():
    """Timer that generate PWM.
    """

#region Constructor
    
    def __init__(self):
        # Init memory.
        self.__timer = Timer()
        self.__ton_cb = None
        self.__toff_cb = None
        self.__upper_limit = 0
        self.__lower_limit = 0
        self.__duty_cycle = 0
        self.__counter = 0
        self.__state = 0

        # Init state.
        self.upper_limit = 900
        self.duty_cycle = 0
        self.counter = 0
        self.period = 1

#endregion

#region Properties
        
    @property
    def period(self):
        """Get period time in seconds.

        Returns:
            float: Period time.
        """
        return self.__timer.expiration_time

    @period.setter
    def period(self, value):
        """Set period time in seconds.

        Args:
            value (float): Period time in seconds.
        """
        # Clear the counter.
        self.counter = 0
        self.__timer.expiration_time = value

    @property
    def duty_cycle(self):
        """Get duty cycle [0-1].

        Returns:
            float: Duty cycle [0-1].
        """
        return round(self.__duty_cycle / self.__upper_limit, 2)

    @duty_cycle.setter
    def duty_cycle(self, value):
        """Set duty cycle [0-1].

        Args:
            value (float): Duty cycle [0-1].
        """

        # Clear the counter.
        self.counter = 0

        if value <= 0:
            value = 0
            self.__duty_cycle = int(value)
        elif value > 0 and value < 1:
            self.__duty_cycle = int(self.__upper_limit * value)
        elif value >= 1:
            value = 1
            self.__duty_cycle = int(self.__upper_limit * value)

    @property
    def counter(self):
        """Get counter.

        Returns:
            int: Ticks
        """
        return self.__counter

    @counter.setter
    def counter(self, value):
        """Set counter.

        Args:
            value (int): Ticks
        """
        self.__counter = value

    @property
    def upper_limit(self):
        """Get upper limit.

        Returns:
            int: Ticks
        """
        return self.__upper_limit

    @upper_limit.setter
    def upper_limit(self, value):
        """Set upper limit.

        Args:
            value (int): Ticks
        """

        # Clear the counter.
        self.counter = 0
        self.__upper_limit = value

    @property
    def is_on(self):
        """Is ON flag.

        Returns:
            bool: True if it ON.
        """
        return (self.__state == TimerPWMState.TIME_TO_ON) or (self.__state == TimerPWMState.UPPER_LIMIT)

    @property
    def is_off(self):
        """Is OFF flag.

        Returns:
            bool: True if it OFF.
        """
        return (self.__state == TimerPWMState.TIME_TO_OFF) or (self.__state == TimerPWMState.LOWER_LIMIT)

    @property
    def state(self):
        """State of the PWM timer.

        Returns:
            int: _description_
        """
        return self.__state

#endregion

#region Public Methods

    def update(self):
        """Update PWM timer.
        """

        self.__timer.update()
        if self.__timer.expired:
            self.__timer.clear()

            # Check for lower limit.
            if self.__duty_cycle <= self.__lower_limit:
                if self.__state != TimerPWMState.LOWER_LIMIT:
                    self.__state = TimerPWMState.LOWER_LIMIT
                    if self.__toff_cb is not None:
                        self.__toff_cb()

            # Check for OFF time.
            elif self.__counter == self.__duty_cycle:
                if self.__state != TimerPWMState.TIME_TO_OFF:
                    self.__state = TimerPWMState.TIME_TO_OFF
                    if self.__toff_cb is not None:
                        self.__toff_cb()

            # Check for upper limit.
            if self.__duty_cycle >= self.__upper_limit:
                if self.__state != TimerPWMState.UPPER_LIMIT:
                    self.__state = TimerPWMState.UPPER_LIMIT
                    if self.__ton_cb is not None:
                        self.__ton_cb()

            # Check for ON time.
            elif self.__counter >= self.__lower_limit and\
                self.__counter < self.__duty_cycle:
                if self.__state != TimerPWMState.TIME_TO_ON:
                    self.__state = TimerPWMState.TIME_TO_ON
                    if self.__ton_cb is not None:
                        self.__ton_cb()

            # Increment timer.
            self.__counter += 1

            # Clear the counter.
            if self.__counter >= self.__upper_limit:
                self.__counter = self.__lower_limit

    def set_cb(self, ton=None, toff=None):
        """Set callback function for tON and tOFF processes.

        Args:
            ton (function, optional): Time ot ON function. Defaults to None.
            toff (function, optional): Time to OFF function. Defaults to None.
        """
        if ton is not None:
            self.__ton_cb = ton

        if toff is not None:
            self.__toff_cb = toff

#endregion
