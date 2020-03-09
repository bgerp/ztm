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

    __logger = None
    """Logger"""

    __free_to_lock = 0
    """Free to lock flag."""

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

    __open_timer_time = 10
    """Open timer time."""

    __open_timer = None
    """Open timer."""


    __lock_mechanism_enabled = False
    """Lock mechanism enabled."""

    __lock_mechanism_output = "DO0"
    """Locking mechanism output."""

    __exit_button_enabled = False
    """Exit button enabled."""

    __exit_button_input = "DI0"
    """Exit button input."""

#endregion

#region Destructor

    def __del__(self):
        del self.__logger
        del self.__card_reader
        del self.__allowed_card_ids
        del self.__cards_queue
        del self.__open_timer

#endregion

#region Private Methods

    def __get_button(self):

        state = 0

        if self.__exit_button_enabled:
            state = self._controller.digital_read(self.__exit_button_input)

        return state

    def __set_latch(self, value=0):
        if self.__lock_mechanism_enabled:
            self._controller.digital_write(self.__lock_mechanism_output, value)

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

    def __time_to_open_cb(self, register):
        self.__open_timer.expiration_time = register.value

    def __exit_button_enabled_cb(self, register):
        self.__exit_button_enabled = register.value

    def __exit_button_input_cb(self, register):
        self.__exit_button_enabled = register.value

    def __card_reader_enabled_cb(self, register):

        if register.value == 1 and self.__card_reader is None:
            key = register.base_name
            card_reader_vendor = self._registers.by_name(key + ".card_reader.vendor").value
            card_reader_model = self._registers.by_name(key + ".card_reader.model").value
            card_reader_serial_number = self._registers.by_name(key + ".card_reader.serial_number").value
            card_reader_port_name = self._registers.by_name(key + ".card_reader.port.name").value
            card_reader_port_baudrate = self._registers.by_name(key + ".card_reader.port.baudrate").value

            # Filter by vendor and model.
            if card_reader_vendor == "TERACOM":
                if card_reader_model == "act230":

                    # Get card reader parameters.
                    reader_config = {
                        "port_name": card_reader_port_name,
                        "baudrate": card_reader_port_baudrate,
                        "serial_number": card_reader_serial_number,
                        "controller": self._controller,
                        "erp_service": self._erp_service
                    }

                    # Create card reader.
                    self.__card_reader = ACT230(reader_config)
                    if self.__card_reader.reader_state is ReaderState.NONE:
                        self.__card_reader.cb_readed_card(self.__create_record)
                        self.__card_reader.start()

        elif register.value == 0 and self.__card_reader is not None:
            self.__card_reader.stop()

            while self.__card_reader.reader_state == ReaderState.RUN:
                pass

            del self.__card_reader

    def __lock_mechanism_enabled_cb(self, register):
        self.__lock_mechanism_enabled = register.value

    def __lock_mechanism_output_cb(self, register):
        self.__lock_mechanism_output = register.value

    def __allowed_attendees_cb(self, register):
        self.add_allowed_card_ids(register.value)

#endregion

#region Public Methods

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

        self.__allowed_card_ids.clear()

        for card_id in ids:
            self.add_allowed_card_id(card_id)

    def init(self):

        # Create logger.
        self.__logger = get_logger(__name__)

        self.__logger.info("Starting the {}".format(self.name))

        # Create queue for the card.
        self.__cards_queue = queue.Queue(self.__cards_queue_size)

        # Set registrator state.
        self.__registrator_state = StateMachine(RegistratorState.GetFromQue)

        # Open timer.
        self.__open_timer = Timer(self.__open_timer_time)

        self.__allowed_card_ids = []

        # Get time to open the latch.
        time_to_open = self._registers.by_name(self._key + ".time_to_open")
        if time_to_open is not None:
            time_to_open.update_handler = self.__time_to_open_cb

        # Create exit button.
        exit_button_enabled = self._registers.by_name(self._key + ".exit_button.enabled")
        if exit_button_enabled is not None:
            exit_button_enabled.update_handler = self.__exit_button_enabled_cb

        exit_button_input = self._registers.by_name(self._key + ".exit_button.input")
        if exit_button_input is not None:
            exit_button_input.update_handler = self.__exit_button_input_cb

        # Create locking mechanism.
        lock_mechanism_enabled = self._registers.by_name(self._key + ".lock_mechanism.enabled")
        if lock_mechanism_enabled is not None:
            lock_mechanism_enabled.update_handler = self.__lock_mechanism_enabled_cb

        lock_mechanism_output = self._registers.by_name(self._key + ".lock_mechanism.output")
        if lock_mechanism_output is not None:
            lock_mechanism_output.update_handler = self.__lock_mechanism_output_cb

        card_reader_enabled = self._registers.by_name(self._key + ".card_reader.enabled")
        if card_reader_enabled is not None:
            card_reader_enabled.update_handler = self.__card_reader_enabled_cb

        # Card reader allowed IDs.
        allowed_attendees = self._registers.by_name(self._key + ".allowed_attendees")
        if allowed_attendees is not None:
            allowed_attendees.update_handler = self.__allowed_attendees_cb

    def update(self):

        if self.__card_reader is None:
            return

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

        if self.__card_reader is not None:
            self.__card_reader.stop()

            while self.__card_reader.reader_state == ReaderState.RUN:
                pass

#endregion
