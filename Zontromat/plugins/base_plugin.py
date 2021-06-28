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

from utils.configuarable import Configuarable

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

class BasePlugin(Configuarable):
    """This class is dedicated to be base class for every zone plugin."""

#region Attributes

    _controller = None
    """Controller
    """

    _registers = None
    """Registers
    """

    __ready_flag = False

    __in_cycle_flag = False

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor
        """

        super().__init__(config)

        if "controller" in config:
            self._controller = config["controller"]

        if "registers" in config:
            self._registers = config["registers"]

    def __del__(self):
        """Destructor
        """

        super().__del__()

#endregion

#region Private Methods (Thread safe routines)

    def __ready(self, value: bool):
        """Set the ready flag state.

        Args:
            value (bool): Flag state.
        """
        
        self.__ready_flag = value

    def __is_ready(self):
        """Returns the ready flag state.

        Returns:
            bool: Ready flag state.
        """

        return self.__ready_flag

    def __in_cycle(self, value: bool):
        """Set the in cycle flag state.

        Args:
            value (bool): Flag state.
        """

        self.__in_cycle_flag = value

    def __wait(self):
        """Wait until in cycle flag is true.
        """

        while self.__in_cycle_flag == True:
            pass

#endregion

#region Protected Methods (Plugin protected interface)

    def _init(self):
        """Initialize the plugin.
        """

        pass

    def _update(self):
        """Update the plugin.
        """

        pass

    def _shutdown(self):
        """Shutdown the plugin.
        """

        pass

#endregion

#region Public Methods

    def init(self):
        """Initialize the plugin.
        """

        # Initialize the plugin.
        self._init()

        # Tell the system that initialization is ready.
        self.__ready(True)

    def update(self):
        """Update the plugin.
        """

        # Ask the runtime engine is it possible to update the logic.
        if not self.__is_ready():
            return

        # Tell the runtime engine that it is entering in cycle.
        self.__in_cycle(True)

        # Update the plugin.
        self._update()

        # Tell the runtime engine that it is exiting from cycle.
        self.__in_cycle(False)

    def shutdown(self):
        """Shutdown the plugin.
        """

        # Tell the runtime engine that it if de initialize and shutdown.
        self.__ready(False)

        # Wait to release the process.
        self.__wait()

        # Shutdown the plugin.
        self._shutdown()

#endregion
