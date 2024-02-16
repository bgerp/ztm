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

from utils.logger import get_logger
from utils.logic.functions import l_scale

from plugins.base_plugin import BasePlugin

from devices.factories.valve.valve_factory import ValveFactory
from devices.factories.pumps.pump_factory import PumpFactory
from devices.utils.valve_control_group.valve_control_group_mode import ValveControlGroupMode

# (Request from mail: Eml6429)

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

class ValveControlGroup(BasePlugin):
    """[summary]

    Args:
        BasePlugin ([type]): [description]

    Returns:
        [type]: [description]
    """

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self.__mode = ValveControlGroupMode.NONE
        """Mode of the valve control group.
        """

        self.__in_valves = {}
        """Forward valves.
        """

        self.__rev_valves = {}
        """Reverse valves.
        """

        if "mode" in config:
            self.mode = config["mode"]

        self.__init_in_vlv()

        self.__init_ret_vlv()

    def __del__(self):
        """Destructor
        """

        if self.__in_valves is not None:
            for valve in self.__in_valves:
                del self.__in_valves[valve]
            del self.__in_valves

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                del self.__rev_valves[valve]
            del self.__rev_valves

        super().__del__()

        if self.__logger is not None:
            del self.__logger

    def __str__(self):

        return self._config["name"]

    __repr__ = __str__

#endregion

#region Properties

    @property
    def target_position(self):

        return 0

    @target_position.setter
    def target_position(self, position):
        """Set the position of the valve control group.

        Args:
            position (int): Position of the valves.
        """

        # In this mode we controll proportional all the forward vales.
        # And invers proportional all revers valves.
        if self.mode == ValveControlGroupMode.Proportional:

            if position > 100.0:
                position = 100.0

            if position < 0.0:
                position = 0.0

            if self.__in_valves is not None:
                for valve in self.__in_valves:
                    valve.target_position = position

            if self.__rev_valves is not None:
                for valve in self.__rev_valves:
                    valve.target_position = float(l_scale(position, [0, 100], [100, 0]))

        # In this mode we controll proportional all the forward vales.
        # And invers proportional all revers valves.
        # But when the value of the
        elif self.mode == ValveControlGroupMode.DualSide:

            if position > 100.0:
                position = 100.0

            if position < -100.0:
                position = -100.0

            if position > 0:
                if self.__in_valves is not None:
                    for valve in self.__in_valves:
                        valve.target_position = position

                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        valve.target_position = 0

            elif position < 0:
                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        valve.target_position = float(l_scale(position, [0, -100], [0, 100]))

                if self.__in_valves is not None:
                    for valve in self.__in_valves:
                        valve.target_position = 0

            else:
                if self.__in_valves is not None:
                    for valve in self.__in_valves:
                        valve.target_position = 0

                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        valve.target_position = 0

    @property
    def mode(self):

        return self.__mode

    @mode.setter
    def mode(self, mode):

        if ValveControlGroupMode.is_valid(mode):
            self.__mode = mode

#endregion

#region 

#region Private 

    def __init_in_vlv(self):

        in_valves = []
        if "in_valves" in self._config:
            in_valves = self._config["in_valves"]

        for name in in_valves:
            reg_name = "{}.{}".format(self._config["key"], name)
            register = self._registers.by_name(reg_name)
            if register is not None:
                valve_name = "{} {}".format(self._config["name"], name)
                valve = ValveFactory.create(
                    name=valve_name,
                    controller=self._controller,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])

                self.__in_valves[valve_name] = valve

    def __init_ret_vlv(self):

        rev_valves = []
        if "rev_valves" in self._config:
            rev_valves = self._config["rev_valves"]

        for name in rev_valves:
            reg_name = "{}.{}".format(self._config["key"], name)
            register = self._registers.by_name(reg_name)
            if register is not None:
                valve_name = "{} {}".format(self._config["name"], name)
                valve = ValveFactory.create(
                    name=valve_name,
                    controller=self._controller,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])

                self.__rev_valves[valve_name] = valve

#endregion

#region Public Methods

    def init(self):
        """Initialize the group.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        self.mode = ValveControlGroupMode.NONE

        if self.__in_valves is not None:
            for valve in self.__in_valves:
                self.__in_valves[valve].init()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].init()

    def update(self):
        """Update valve state.
        """

        if self.__in_valves is not None:
            for valve in self.__in_valves:
                self.__in_valves[valve].update()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].update()

    def shutdown(self):
        """Shutdown the group.
        """

        if self.__in_valves is not None:
            for valve in self.__in_valves:
                self.__in_valves[valve].shutdown()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].shutdown()

    def calibrate(self):

        if self.__in_valves is not None:
            for valve in self.__in_valves:
                valve.calibrate()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.calibrate()

#endregion

#region Public Static Methods

#endregion
