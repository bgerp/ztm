
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

from devices.base_device import BaseDevice

from devices.utils.card_readers.card_reader_state import CardReaderState

from utils.logic.state_machine import StateMachine

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

class BaseCardReader(BaseDevice):
    """Card reader base class."""

#region Attributes

    _serial_number = None
    """Card reader ID."""

    _port_name = None
    """Port name."""

    _cb_read_card = None
    """Read card callback."""

    _state = None
    """Reader state."""

#endregion

#region Constructor

    def __init__(self, kwargs):

        super().__init__(kwargs)

        self._state = StateMachine(CardReaderState.NONE)

        if "port_name" in kwargs:
            self._port_name = kwargs["port_name"]

        if "serial_number" in kwargs:
            self._serial_number = kwargs["serial_number"]

#endregion

#region Properties

    @property
    def serial_number(self):
        """Returns the card reader ID.

        Returns
        -------
        str
            Returns the card reader ID.
        """
        return self._serial_number

    @property
    def port_name(self):
        """Returns the card reader port name.

        Returns
        -------
        Enum
            Returns the card reader port name.
        """

        if self._port_name is None:
            return ""

        return self._port_name

    @property
    def reader_state(self):
        """Start the reader."""

        return self._state.get_state()

#endregion

#region Public Methods

    def cb_read_card(self, callback):
        """Add the card reader callback when card is inserted.

        Parameters
        ----------
        callback : function pointer
            Called function.
        """

        if callback is None:
            raise ValueError("Callback can not be None.")

        self._cb_read_card = callback

#endregion
