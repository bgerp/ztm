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
from devices.factories.pump.pump_factory import PumpFactory
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

    __logger = None
    """Logger
    """

    __mode = ValveControlGroupMode.NONE
    """Mode of the valve control group.
    """

    __fw_valves = {}
    """Forward valves.
    """

    __rev_valves = {}
    """Reverse valves.
    """

    __fw_pumps = {}
    """Forward pumps control.
    """

    __rev_pumps = {}
    """Revers pumps control.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self.__fw_valves = {}
        self.__rev_valves = {}
        self.__fw_pumps = {}
        self.__rev_pumps = {}

        fw_valves = []
        if "fw_valves" in self._config:
            fw_valves = self._config["fw_valves"]

        for name in fw_valves:
            reg_name = "{}.{}".format(config["key"], name)
            register = self._registers.by_name(reg_name)
            if register is not None:

                valve_name = "{} {}".format(config["name"], name)
                valve = ValveFactory.create(
                    name=valve_name,
                    controller=self._controller,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])

                self.__fw_valves[valve_name] = valve

        rev_valves = []
        if "rev_valves" in self._config:
            rev_valves = self._config["rev_valves"]

        for name in rev_valves:
            reg_name = "{}.{}".format(config["key"], name)
            register = self._registers.by_name(reg_name)
            if register is not None:

                valve_name = "{} {}".format(config["name"], name)
                valve = ValveFactory.create(
                    name=valve_name,
                    controller=self._controller,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])

                self.__rev_valves[valve_name] = valve

        fw_pumps = []
        if "fw_pumps" in self._config:
            fw_pumps = self._config["fw_pumps"]

        for name in fw_pumps:
            reg_name = "{}.{}".format(config["key"], name)
            register = self._registers.by_name(reg_name)
            if register is not None:

                pump_name = "{} {}".format(config["name"], name)
                pump = PumpFactory.create(
                    name=pump_name,
                    controller=self._controller,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])

                self.__fw_pumps[pump_name] = pump

        rev_pumps = []
        if "rev_pumps" in self._config:
            rev_pumps = self._config["rev_pumps"]

        for name in rev_pumps:
            reg_name = "{}.{}".format(config["key"], name)
            register = self._registers.by_name(reg_name)
            if register is not None:

                pump_name = "{} {}".format(config["name"], name)
                pump = PumpFactory.create(
                    name=pump_name,
                    controller=self._controller,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])

                self.__rev_pumps[pump_name] = pump

    def __del__(self):
        """Destructor
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                del self.__fw_valves[valve]
            del self.__fw_valves

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                del self.__rev_valves[valve]
            del self.__rev_valves

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                del self.__fw_pumps[valve]
            del self.__fw_pumps

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                del self.__rev_pumps[valve]
            del self.__rev_pumps


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

            if self.__fw_valves is not None:
                for valve in self.__fw_valves:
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
                if self.__fw_valves is not None:
                    for valve in self.__fw_valves:
                        valve.target_position = position

                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        valve.target_position = 0

            elif position < 0:
                if self.__rev_valves is not None:
                    for valve in self.__rev_valves:
                        valve.target_position = float(l_scale(position, [0, -100], [0, 100]))

                if self.__fw_valves is not None:
                    for valve in self.__fw_valves:
                        valve.target_position = 0

            else:
                if self.__fw_valves is not None:
                    for valve in self.__fw_valves:
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

    @property
    def debit(self):
        """Get debit.

        Returns:
            float: Debit of the group.
        """

        return 0

    @debit.setter
    def debit(self, debit):
        """Set debit.

        Args:
            debit (float): Debit of the pump.
        """

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                pump.debit = debit

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                pump.debit = float(l_scale(debit, [0, 100], [100, 0]))

#endregion

#region Public Methods

    def init(self):
        """Initialize the group.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        self.mode = ValveControlGroupMode.NONE

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].init()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].init()

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                self.__fw_pumps[pump].init()

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                self.__rev_pumps[pump].init()

    def update(self):
        """Update valve state.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].update()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].update()

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                self.__fw_pumps[pump].update()

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                self.__rev_pumps[pump].update()

    def shutdown(self):
        """Shutdown the group.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                self.__fw_valves[valve].shutdown()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                self.__rev_valves[valve].shutdown()

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                self.__fw_pumps[pump].shutdown()

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                self.__rev_pumps[pump].shutdown()

    def calibrate(self):

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                pump.debit = 0

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                pump.debit = 0

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.calibrate()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.calibrate()

#endregion

#region Public Static Methods

#endregion
