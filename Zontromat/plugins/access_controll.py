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
import queue

from enum import Enum

from utils.logger import get_logger
from utils.state_machine import StateMachine
from utils.timer import Timer

from plugins.base_plugin import BasePlugin

from devices.TERACOM.act230 import ACT230
from devices.TERACOM.act230 import ReaderState

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

class RegistratorState(Enum):
    """Registrator state enumeration class."""

    GetFromQue = 1
    Send = 2

class AccessControll(BasePlugin):
    """Power meter device."""

#region Attributes

    __free_to_lock = 0
    """Free to lock flag."""

    __logger = None
    """Logger"""

    __open_door_flag = 0
    """Open door flag."""

    __card_reader = None
    """Card reader 1."""

    __allowed_card_ids = None
    """Card reader 1."""

    __cards_queue = None
    """Register queue."""

    __cards_queue_size = 10000
    """Uplink queue size."""

    __registrator_state = None
    """Registrator state."""

    __first_queue_record = None
    """Firs record."""

    __lock_mechanism_enabled = False
    """Lock mechanism enabled."""

    __exit_button_enabled = False
    """Exit button enabled."""

#endregion

#region Private Methods

    def __get_button(self):

        state = 0

        if self.__exit_button_enabled:
            state = self._controller.digital_read(self._config["exit_button_input"])

        return state

    def __set_latch(self, value=0):
        if self.__lock_mechanism_enabled:
            self._controller.digital_write(self._config["lock_mechanism_output"], value)

    def __create_record(self, card_id):

        # Set flag to open the door.
        if self.__allowed_card_ids is not None:
            if card_id in self.__allowed_card_ids:
                if self.__open_door_flag == 0:
                    self.__open_door_flag = 1

        # Create a record.
        record = { \
            "time": time.time(), \
            "parameters": { \
                "card_id": card_id, \
                "reader_id": self.__card_reader.reader_id, \
            } \
        }

        # Check the queue and take action.
        if self.__cards_queue.full():
            self.__logger.warning("The queue is full.")
        else:
            self.__logger.debug("Received ID: {}".format(record))
            self.__cards_queue.put(record)

#endregion

#region Public Methods

    def update_allowed_card_ids(self, ids):
        """Updated allowed card IDs.

        Parameters
        ----------
        ids : array
            Cards ids.

        """

        self.__allowed_card_ids = ids

    def add_allowed_card_id(self, card_id):
        """Add allowed card ID.

        Parameters
        ----------
        ids : str
            Cards id.

        """

        if card_id is None:
            return

        if card_id == "":
            return

        if card_id in self.__allowed_card_ids:
            pass

        else:
            self.__allowed_card_ids.append(card_id)

    def add_allowed_card_ids(self, ids):
        """Add allowed cards IDs.

        Parameters
        ----------
        ids : array
            Cards id.

        """

        if ids is None:
            return

        for card_id in ids:
            self.add_allowed_card_id(card_id)

    def remove_allowed_card_id(self, card_id):
        """Remove allowed card ID.

        Parameters
        ----------
        ids : str
            Cards card_id.

        """

        if id in self.__allowed_card_ids:
            self.__allowed_card_ids(card_id)

    def remove_allowed_card_ids(self, ids):
        """Remove allowed card ID.

        Parameters
        ----------
        ids : array
            Cards id.

        """

        if ids is None:
            return

        if id in ids:
            self.remove_allowed_card_id(id)

    def init(self):

        # Create logger.
        self.__logger = get_logger(__name__)

        self.__logger.info("Starting the {}".format(self.name))

        # Set registrator state.
        self.__registrator_state = StateMachine(RegistratorState.GetFromQue)

        # Open timer.
        self.__open_timer = Timer(10)

        # Get time to open the latch.
        if "time_to_open" in self._config:
            self.__open_timer.expiration_time = self._config["time_to_open"]

        # Create exit button.
        if "exit_button_enabled" in self._config:
            self.__exit_button_enabled = self._config["exit_button_enabled"]

        # Create locking mechanism.
        if "lock_mechanism_enabled" in self._config:
            self.__lock_mechanism_enabled = self._config["lock_mechanism_enabled"]

        # Create Cart reader.
        if "card_reader_enabled" in self._config:
            card_reader_enabled = self._config["card_reader_enabled"]
            if card_reader_enabled:

                # Filter by vendor and model.
                card_reader_vendor = self._config["card_reader_vendor"]
                if card_reader_vendor == "TERACOM":
                    card_reader_model = self._config["card_reader_model"]
                    if card_reader_model == "act230":

                        # Get card reader parameters.
                        reader_config = {
                            "port_name": self._config["card_reader_port_name"],
                            "baudrate": self._config["card_reader_port_baudrate"],
                            "serial_number": self._config["card_reader_serial_number"],
                            "controller": self._config["controller"],
                            "erp_service": self._config["erp_service"]
                        }

                        # Create card reader.
                        self.__card_reader = ACT230(reader_config)
                        if self.__card_reader.reader_state is ReaderState.NONE:
                            self.__card_reader.cb_readed_card(self.__create_record)
                            self.__card_reader.start()

        # Card reader allowed IDs.
        if "card_reader_allowed_ids" in self._config:
            self.__allowed_card_ids = self._config["card_reader_allowed_ids"]

        # Create queue for the card.
        if "carts_queue_size" in self._config:
            self.__cards_queue_size = self._config["carts_queue_size"]
            self.__cards_queue = queue.Queue(self.__cards_queue_size)
        else:
            self.__cards_queue = queue.Queue(self.__cards_queue_size)

    def update(self):

        # Update crad reader.
        self.__card_reader.update()

        if self.__card_reader.reader_state == ReaderState.STOP:
            self.__logger.warning("Card reader {}; State {}; Port {}."\
                .format(self.__card_reader.reader_id, \
                        self.__card_reader.reader_state, \
                        self.__card_reader.port_name))

            self.__card_reader.start()

        if self.__card_reader.reader_state == ReaderState.NONE:
            self.__logger.warning("Card reader {}; State {}."\
                .format(self.__card_reader.reader_id, self.__card_reader.reader_state))

            self.__card_reader.start()

        # Check if the button is pressed.
        btn_value = self.__get_button()
        if btn_value == 1:
            if self.__open_door_flag == 0:
                self.__open_door_flag = 1

        # Check if the flag is raiced.
        if self.__open_door_flag == 1:
            self.__set_latch(1)
            self.__open_timer.update_last_time()
            self.__open_door_flag = 0
            self.__free_to_lock = 1

        # Check is it time to close the latch.
        if self.__open_door_flag == 0:
            self.__open_timer.update()
            if self.__open_timer.expired:
                self.__open_timer.clear()

                if self.__free_to_lock == 1:
                    self.__set_latch(0)
                    self.__free_to_lock = 0

        if self.__cards_queue.empty() is not True:

            if self.__registrator_state.is_state(RegistratorState.GetFromQue):

                self.__first_queue_record = self.__cards_queue.get()
                self.__registrator_state.set_state(RegistratorState.Send)

            if self.__registrator_state.is_state(RegistratorState.Send):

                # Send event to the ERP service.
                rec = [self.__first_queue_record]
                sucessfull = self._erp_service.sync(rec)

                if sucessfull is not None:
                    self.__logger.debug("Send ID: {}".format(self.__first_queue_record))
                    self.__registrator_state.set_state(RegistratorState.GetFromQue)

    def shutdown(self):
        """Shutdown the reader."""

        self.__logger.info("Shutdown the {}".format(self.name))

        self.__set_latch(0)
        self.__card_reader.stop()

        while self.__card_reader.reader_state == ReaderState.RUN:
            pass

#endregion
