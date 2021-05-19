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
from enum import Enum

from utils.logger import get_logger
from utils.logic.functions import l_scale

from plugins.base_plugin import BasePlugin

from devices.factories.valve.valve_factory import ValveFactory
from devices.factories.pump.pump_factory import PumpFactory

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

__class_name__ = "EnergyCenter"
"""Plugin class name."""

#endregion

class ValveControlGroup(BasePlugin):

#region Attributes

    __logger = None
    """Logger
    """

    __fw_valves = []
    """Forward valves.
    """

    __rev_valves = []
    """Reverse valves.
    """

    __fw_pumps = []
    """Forward pumps control.
    """    

    __rev_pumps = []
    """Revers pumps control.
    """    

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config) 

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        if "fw_pumps" in self._config:
            self.__fw_pumps = self._config["fw_pumps"]

        if "rev_pumps" in self._config:
            self.__rev_pumps = self._config["rev_pumps"]

        if "fw_valves" in self._config:
            self.__fw_valves = self._config["fw_valves"]

        if "rev_valves" in self._config:
            self.__rev_valves = self._config["rev_valves"]

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                del valve

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                del valve

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                del valve

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                del valve

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

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.target_position = position

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.target_position = float(l_scale(position, [0, 100], [100, 0]))

#endregion

#region Public Methods

    def set_debit(self, debit):
        """Set debit.

        Args:
            debit (int): Debit of the pump.
        """

        if self.__fw_pumps is not None:
            for pump in self.__fw_pumps:
                pump.debit = debit

        if self.__rev_pumps is not None:
            for pump in self.__rev_pumps:
                pump.debit = float(l_scale(debit, [0, 100], [100, 0]))

    def init(self):
        """Init the group.
        """

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                valve.init()

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                valve.init()

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.init()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.init()

    def update(self):
        """Update valve state.
        """

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                valve.update()

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                valve.update()

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.update()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.update()

    def shutdown(self):
        """Shutdown the group.
        """

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                valve.shutdown()

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                valve.shutdown()

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.shutdown()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.shutdown()

#endregion

#region Public Static Methods

    @staticmethod
    def create(**config):
        """Create the group by given settings.

        Returns:
            ValveControlGroup: Instance of the control group.
        """

        group_name = ""
        if "name" in config:
            group_name = config["name"]

        key = None
        if "key" in config:
            key = config["key"]

        controller = None
        if "controller" in config:
            controller = config["controller"]

        registers = None
        if "registers" in config:
            registers = config["registers"]

        fw_valves = []
        if "fw_valves" in config:
            fw_valves = config["fw_valves"]

        rev_valves = []
        if "rev_valves" in config:
            rev_valves = config["rev_valves"]


        registers = config["registers"]

        f_valves = []
        for name in fw_valves:
            reg_name = "{}.{}".format(config["key"], name)
            register = registers.by_name(reg_name)
            if register is not None:

                params = register.value.split("/")

                if len(params) < 2:                
                    raise ValueError("Not enough parameters.")

                f_valves.append(ValveFactory.create(
                    name="{} {}".format(config["name"], name),
                    controller=controller,
                    params=params))

        r_valves = []
        for name in rev_valves:
            reg_name = "{}.{}".format(config["key"], name)
            register = registers.by_name(reg_name)
            if register is not None:

                params = register.value.split("/")

                if len(params) < 2:                
                    raise ValueError("Not enough parameters.")

                r_valves.append(ValveFactory.create(
                    name="{} {}".format(config["name"], name),
                    controller=controller,
                    params=params))


        control_group = ValveControlGroup(
            name=group_name,
            key=key,
            registers=registers,
            controller=controller,
            fw_valves=f_valves,
            rev_valves=r_valves)

        return control_group

#endregion
