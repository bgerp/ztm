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

from enum import Enum

import serial

from utils.logger import get_logger

from devices.base_device import BaseDevice

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class ReaderState(Enum):
    """Card reader states."""

    NONE = 0
    START = 1
    RUN = 2
    STOP = 3

class ACT230(BaseDevice):
    """Teracom RFID card reader model ACA100."""

#region Attributes

    __logger = None
    """Logger"""

    __port = None
    """Actual serial port."""

    __cb_read_card = None
    """Read card callback."""

    __card_number_len = 16
    """RFID number length."""

    __reader_id = None
    """Card reader ID."""

    __reader_state = ReaderState.NONE
    """Card reader state flag."""

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor"""

        super().__init__(config)

        self.__logger = get_logger(__name__)

    def __del__(self):
        """Destructor"""

        self.stop()

#endregion

#region Properties

    @property
    def reader_id(self):
        """Returns the card reader ID.

        Returns
        -------
        str
            Returns the card reader ID.
        """
        return self.__reader_id

    @property
    def reader_state(self):
        """Returns the card reader state.

        Returns
        -------
        Enum
            Returns the card reader state.
        """

        return self.__reader_state

    @property
    def port_name(self):
        """Returns the card reader port name.

        Returns
        -------
        Enum
            Returns the card reader port name.
        """

        if self.__port is None:
            return ""

        return self.__port.name

#endregion

#region Private Methods

    def __set_state(self, state):

        if state is not self.__reader_state:
            self.__reader_state = state

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

        self.__cb_read_card = callback

    def stop(self):
        """Stop the reader."""

        self.__set_state(ReaderState.STOP)

    def start(self):
        """Start the reader."""

        self.__set_state(ReaderState.START)

    def update(self):
        """Update card reader processing."""

        # Stop
        if self.__reader_state == ReaderState.STOP:
            try:
                if self.__port.is_open:
                    self.__port.close()

                    self.__port = None

                    while self.__port is not None:
                        pass

                    del self.__port

            except:
                self.__set_state(ReaderState.NONE)

        # Start
        elif self.__reader_state == ReaderState.START:
            try:
                # Create port.
                self.__port = serial.Serial(\
                    port=self._config["port_name"],\
                    baudrate=self._config["baudrate"],
                    timeout=1)

                self.__reader_id = self._config["serial_number"]

                # Open the port.
                if not self.__port.is_open:
                    self.__port.open()

                # Change the state to RUN.
                self.__set_state(ReaderState.RUN)

            except:
                # If something goes wrong go to NONE.
                self.__set_state(ReaderState.NONE)

        # Run
        elif self.__reader_state == ReaderState.RUN:
            try:
                if self.__cb_read_card is not None:
                    frame = None

                    size = self.__port.inWaiting()

                    if size > 0:
                        frame = self.__port.read(size)
                        frame = frame.decode("utf-8")
                        frame = frame.replace("\r", "").replace("\n", "").replace("?", "")
                        if len(frame) == self.__card_number_len:
                            self.__cb_read_card(frame, self.reader_id)

            except Exception as e:
                print(e)
                self.stop()

#endregion
