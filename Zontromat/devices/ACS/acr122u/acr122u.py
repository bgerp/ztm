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

from enum import Enum
from threading import Thread
import sys, traceback

import nfc
import ndef

from utils.logger import get_logger

from devices.utils.card_readers.base_card_reader import BaseCardReader
from devices.utils.card_readers.card_reader_state import CardReaderState

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

class ACR122U(BaseCardReader):
    """ACR122 NFC Card Reader"""

#endregion

    __logger = None
    """Logger"""

    __clf = None
    """Contactless front-end."""

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self.__logger = get_logger(__name__)

#endregion

    def __beam(self, llc):

        # snep_client = nfc.snep.SnepClient(llc)
        # snep_client.put_records([ndef.TextRecord("Traby")])

        # return
        if self._state.is_state(CardReaderState.START):
            ndef_obj = llc.ndef
            if ndef_obj is not None:
                print(ndef_obj)
                records = ndef_obj.records
                if records is not None:
                    for record in records:
                        if record.type == "urn:nfc:wkt:T":
                            content = record.data.decode("utf-8")
                            print(content)

                # snep_client.put_records([ndef.UriRecord("http://nfcpy.org")])

    def __on_startup(self, target):

        print(target)

        return target

    def __connected(self, llc):

        state = False

        try:
            if self._state.is_state(CardReaderState.START):
                state = True
                Thread(target=self.__beam, args=(llc,)).start()

        except:
            pass

        return state

#region Public Methods

    def init(self):
        """Initialize the device."""

        self._state.set_state(CardReaderState.START)

    def update(self):
        """Update card reader processing."""

        # STOP
        if self._state.is_state(CardReaderState.STOP):
            try:
                if self.__clf is not None:
                    del self.__clf
                    self.__clf = None

            except:
                pass

        # START
        elif self._state.is_state(CardReaderState.START):
            try:
                # Create port.
                # Port name: usb:072f:2200
                self.__clf = nfc.ContactlessFrontend(self.port_name)

                # Connect to the WFE.
                state = self.__clf.connect(rdwr={'on-startup': self.__on_startup, "on-connect": self.__connected})

                # If something goes wrong go to NONE.
                self._state.set_state(CardReaderState.RUN)

            except Exception as e:
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)

                # If something goes wrong go to NONE.
                self._state.set_state(CardReaderState.STOP)

        # START
        elif self._state.is_state(CardReaderState.RUN):
           pass

    def shutdown(self):
        """Stop the reader."""

        if self._state is not None:
            self._state.set_state(CardReaderState.STOP)
