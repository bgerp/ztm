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
import traceback
from threading import Thread

import nfc
# import ndef

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

class ACR122U(BaseCardReader):
    """ACR122 NFC Card Reader"""

#region Attributes

    __logger = None
    """Logger"""

    __clf = None
    """Contactless front-end."""

    __worker_thread = None
    """Worker thread."""

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "ACS"

        self._model = "ACR122U"

        self.__logger = get_logger(__name__)

#endregion

#region Private Messages

    def __on_connected(self, llc):

        state = False

        ndef_obj = llc.ndef
        if ndef_obj is not None:

            records = ndef_obj.records
            if records is not None:

                for record in records:

                    if record.type == "text/vcard":
                        content = record.data.decode("utf-8")
                        self.__logger.debug(content)

                    if record.type == "urn:nfc:wkt:T":
                        content = record.data.decode("utf-8")
                        content = content.replace("en", "")
                        content = content.replace("\x02", "")
                        self._cb_read_card(content, self.serial_number)

                        state = True

        return state

    def __on_startup(self, target):

        self.__logger.debug("Starting NFC: {}".format(time.time()))
        return target

    def __run(self):

        try:
            if self.__clf is not None:
                return

            # Port name: usb:072f:2200
            self.__clf = nfc.ContactlessFrontend(self.port_name)

            # Connect to the WFE.
            self.__clf.connect(rdwr={"on-startup": self.__on_startup, "on-connect": self.__on_connected})

            if self.__clf is not None:

                self.__clf.close()

                del self.__clf
                self.__clf = None

                self._state.set_state(CardReaderState.START)

        except:
            # When the horse when in to the river go to NONE state.
            self._state.set_state(CardReaderState.STOP)
            self.__logger.error(traceback.format_exc())

    def __start(self):

        try:
            self.__worker_thread = Thread(target=self.__run, args=())
            self.__worker_thread.setDaemon(True)
            self.__worker_thread.start()

            self._state.set_state(CardReaderState.RUN)

        except:
            # When the horse when in to the river go to STOP state.
            self._state.set_state(CardReaderState.STOP)
            self.__logger.error(traceback.format_exc())

#endregion

#region Public Methods

    def init(self):
        """Initialize the device."""

        self._state.set_state(CardReaderState.START)

    def update(self):
        """Update card reader processing."""

        # STOP
        if self._state.is_state(CardReaderState.STOP):
            self.shutdown()

        # START
        elif self._state.is_state(CardReaderState.START):
            self.__start()

        # RUN
        elif self._state.is_state(CardReaderState.RUN):
            pass

    def shutdown(self):
        """Stop the reader."""

        try:
            if self.__worker_thread is not None:
                self.__worker_thread = None

            if self.__clf is not None:
                self.__clf.close()
                del self.__clf
                self.__clf = None

        except:
            self.__logger.error(traceback.format_exc())
