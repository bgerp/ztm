#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import traceback
from enum import Enum

import serial

from utils.logger import get_logger

from devices.factories.card_readers.base_card_reader import BaseCardReader
from devices.factories.card_readers.card_reader_state import CardReaderState

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

class ACT230(BaseCardReader):
    """Teracom RFID card reader model ACA100."""

#region Attributes

    __logger = None
    """Logger"""

    __card_number_len = 16
    """RFID number length."""

    __serial_port = None

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Teracom"

        self._model = "ACT230"

        self.__logger = get_logger(__name__)

#endregion

#region Public Methods

    def init(self):
        """Start the reader."""

        self._state.set_state(CardReaderState.START)

    def update(self):
        """Update card reader processing."""

        # Stop
        if self._state.is_state(CardReaderState.STOP):
            try:
                if self.__serial_port.is_open:
                    self.__serial_port.close()

                    self.__serial_port = None

                    while self.__serial_port is not None:
                        pass

                    del self.__serial_port

            except:
                self._state.set_state(CardReaderState.NONE)

        # Start
        elif self._state.is_state(CardReaderState.START):
            try:
                # Create port.
                self.__serial_port = serial.Serial(\
                    port=self._config["port_name"],\
                    baudrate=self._config["baudrate"],
                    timeout=1)

                # Open the port.
                if not self.__serial_port.is_open:
                    self.__serial_port.open()

                # Change the state to RUN.
                self._state.set_state(CardReaderState.RUN)

            except:
                # If something goes wrong go to NONE.
                self._state.set_state(CardReaderState.NONE)

        # Run
        elif self._state.is_state(CardReaderState.RUN):
            try:
                if self._cb_read_card is not None:
                    frame = None

                    size = self.__serial_port.inWaiting()

                    if size > 0:
                        frame = self.__serial_port.read(size)
                        frame = frame.decode("utf-8")
                        frame = frame.replace("\r", "").replace("\n", "").replace("?", "")
                        if len(frame) == self.__card_number_len:
                            self._cb_read_card(frame, self.serial_number)

            except:
                self.__logger.error(traceback.format_exc())
                self.shutdown()

    def shutdown(self):
        """Stop the reader."""

        self._state.set_state(CardReaderState.STOP)

#endregion
