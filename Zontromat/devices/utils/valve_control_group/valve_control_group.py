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

    returns:
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

        self.__fw_valves = {}
        """Forward valves.
        """

        self.__rev_valves = {}
        """return valves.
        """

        if "mode" in config:
            self.mode = ValveControlGroupMode(config["mode"])

        self.__init_fw_vlv()

        self.__init_rev_vlv()

    def __str__(self):

        return self._config["name"]

    __repr__ = __str__

#endregion

#region Properties

    @property
    def target_position(self):

        position = 0

        if self.__mode == ValveControlGroupMode.DualSide:
            positions = [0,0]
            if self.__fw_valves is not None:
                for valve in self.__fw_valves:
                    positions[0] += self.__fw_valves[valve].current_position
                positions[0] *= -1

            if self.__rev_valves is not None:
                for valve in self.__rev_valves:
                    positions[1] += self.__rev_valves[valve].current_position

            position = sum(positions) / len(positions)

            if position > 0:
                position = 100.0

            if position < 0:
                position = -100.0

            position = int(position)

        return position

    @target_position.setter
    def target_position(self, position):
        """Set the position of the valve control group.

        Args:
            position (int): Position of the valves.
        """

        # In this mode we control proportional all the forward vales.
        # And inverse proportional all revers valves.
        if self.mode == ValveControlGroupMode.Proportional:

            if position > 100.0:
                position = 100.0

            if position < 0.0:
                position = 0.0

            if self.__fw_valves is not None:
                for valve in self.__fw_valves:
                    self.__fw_valves[valve].target_position = int(position)

            if self.__rev_valves is not None:
                for valve in self.__rev_valves:
                    self.__rev_valves[valve].target_position = int(l_scale(position, [0, 100], [100, 0]))

        # In this mode we control proportional all the forward vales.
        # And inverse proportional all revers valves.
        # But when the value of the
        elif self.mode == ValveControlGroupMode.DualSide:

            if position > 100.0:
                position = 100.0

            if position < -100.0:
                position = -100.0

            if position > 0:
                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        self.__rev_valves[valve].target_position = 0

                if self.__fw_valves is not None:
                    for valve in self.__fw_valves:
                        self.__fw_valves[valve].target_position = int(position)


            elif position < 0:
                if self.__fw_valves is not None:
                    for valve in self.__fw_valves:
                        self.__fw_valves[valve].target_position = 0

                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        self.__rev_valves[valve].target_position = int(l_scale(position, [0, -100], [0, 100]))

            else:
                if self.__fw_valves is not None:
                    for valve in self.__fw_valves:
                        self.__fw_valves[valve].target_position = 0

                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        self.__rev_valves[valve].target_position = 0

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

    def __init_fw_vlv(self):

        fw_valves = []
        if "fw_valves" in self._config:
            fw_valves = self._config["fw_valves"]

        register = self._registers.by_name(self._config["key"])
        if register is not None:
            for name in fw_valves:
                for key, valve in enumerate(register.value[name]):
                    dev_name=f"{register.name}.{name}.{key}"
                    valve = ValveFactory.create(
                        name=dev_name,
                        controller=self._controller,
                        vendor=valve['vendor'],
                        model=valve['model'],
                        options=valve['options'])
                    self.__fw_valves[dev_name] = valve

    def __init_rev_vlv(self):

        rev_valves = []
        if "rev_valves" in self._config:
            rev_valves = self._config["rev_valves"]

        register = self._registers.by_name(self._config["key"])
        if register is not None:
            for name in rev_valves:
                for key, valve in enumerate(register.value[name]):
                    dev_name=f"{register.name}.{name}.{key}"
                    valve = ValveFactory.create(
                        name=dev_name,
                        controller=self._controller,
                        vendor=valve['vendor'],
                        model=valve['model'],
                        options=valve['options'])
                    self.__rev_valves[dev_name] = valve
#endregion

#region Protected Methods

    def _init(self):
        """Initialize the group.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].init()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].init()

    def _update(self):
        """Update valve state.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].update()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].update()

    def _shutdown(self):
        """Shutdown the group.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].shutdown()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].shutdown()

#endregion

#region Public Methods

    def calibrate(self):

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].calibrate()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].calibrate()

#endregion
