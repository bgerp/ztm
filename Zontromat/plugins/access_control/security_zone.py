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

from data import verbal_const

from devices.TERACOM.act230 import ACT230
from devices.TERACOM.act230 import ReaderState

from utils.logger import get_logger
from utils.timer import Timer

from plugins.base_plugin import BasePlugin

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

class SecurityZone(BasePlugin):
    """Security zone definition class."""

#region Attribute

    __logger = None
    """Logger"""

    __registers = None
    """Registers"""

    __identifier = 0
    """Security zone identifier."""

    __key = ""

    __allowed_attendant = []
    """Allowed attendant."""

    __entry_reader = None
    """Entry card reader."""

    __exit_reader = None
    """Exit card reader."""

    __exit_btn_input = verbal_const.OFF # "DI0"
    """Exit button input."""

    __lock_mechanism_output = verbal_const.OFF # "DO0"
    """Locking mechanism output."""

    __door_closed_input = verbal_const.OFF # "DI2"
    """Door closed input."""

    __free_to_lock = 0
    """Free to lock flag."""

    __open_door_flag = 0
    """Open door flag."""

    __open_timer = None
    """Open timer."""

    __pir_input = verbal_const.OFF # "DI0"
    """PIR"""

    __win_closed_input = verbal_const.OFF # "DI3"
    """Window closed sensor."""

    __reader_read_cb = None
    """Reader read callback"""

    __name = ""
#endregion

#region Constructor

    def __init__(self, registers, controller, identifier):

        self.__registers = registers
        self.__identifier = identifier
        self.__controller = controller

#endregion

#region Destructor

    def __del__(self):
        """Destructor"""

        del self.__logger

        if self.__entry_reader is not None:
            del self.__entry_reader

        if self.__exit_reader is not None:
            del self.__exit_reader

        if self.__open_timer is not None:
            del self.__open_timer

#endregion

#region Private Methods

    def __is_allowed(self, card_id):

        allowed = False

        for card in self.__allowed_attendant:
            if card["card_id"] == card_id:
                allowed = True
                break

        return allowed

    def __rader_read(self, card_id, reader_id):

        # Set flag to open the door.
        if self.__is_allowed(card_id):
            if self.__open_door_flag == 0:
                self.__open_door_flag = 1

        if self.__reader_read_cb is not None:
            self.__reader_read_cb(card_id, reader_id)

    def __entry_reader_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if register.value != verbal_const.NO and self.__entry_reader is None:
            key = register.base_name

            params = register.value.split("/")

            card_reader_vendor = params[0]
            card_reader_model = params[1]
            card_reader_serial_number = params[2]
            card_reader_port_name = self.__registers.by_name("{}.entry_reader_{}.port.name".format(key, self.__identifier)).value
            card_reader_port_baudrate = self.__registers.by_name("{}.entry_reader_{}.port.baudrate".format(key, self.__identifier)).value

            # Filter by vendor and model.
            if card_reader_vendor == "TERACOM":
                if card_reader_model == "act230":

                    # Get card reader parameters.
                    reader_config = {
                        "port_name": card_reader_port_name,
                        "baudrate": card_reader_port_baudrate,
                        "serial_number": card_reader_serial_number,
                        "controller": self.__controller,
                    }

                    # Create card reader.
                    self.__entry_reader = ACT230(reader_config)
                    if self.__entry_reader.reader_state is ReaderState.NONE:
                        self.__entry_reader.cb_read_card(self.__rader_read)
                        self.__entry_reader.start()

        elif register.value == verbal_const.NO and self.__entry_reader is not None:
            self.__entry_reader.stop()

            while self.__entry_reader.reader_state == ReaderState.RUN:
                pass

            del self.__entry_reader

    def __exit_reader_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if register.value != verbal_const.NO and self.__exit_reader is None:
            key = register.base_name

            params = register.value.split("/")

            card_reader_vendor = params[0]
            card_reader_model = params[1]
            card_reader_serial_number = params[2]

            card_reader_port_name = self.__registers.by_name("{}.exit_reader_{}.port.name".format(key, self.__identifier)).value
            card_reader_port_baudrate = self.__registers.by_name("{}.exit_reader_{}.port.baudrate".format(key, self.__identifier)).value

            # Filter by vendor and model.
            if card_reader_vendor == "TERACOM":
                if card_reader_model == "act230":

                    # Get card reader parameters.
                    reader_config = {
                        "port_name": card_reader_port_name,
                        "baudrate": card_reader_port_baudrate,
                        "serial_number": card_reader_serial_number,
                        "controller": self.__controller,
                    }

                    # Create card reader.
                    self.__exit_reader = ACT230(reader_config)
                    if self.__exit_reader.reader_state is ReaderState.NONE:
                        self.__exit_reader.cb_read_card(self.__rader_read)
                        self.__exit_reader.start()

        elif register.value == verbal_const.NO and self.__exit_reader is not None:
            self.__exit_reader.stop()

            while self.__exit_reader.reader_state == ReaderState.RUN:
                pass

            del self.__exit_reader

    def __exit_btn_input_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if self.__exit_btn_input != register.value:
            self.__exit_btn_input = register.value

    def __exit_btn_state(self):

        state = False

        if self.__controller.is_valid_gpio(self.__exit_btn_input):
            state = self.__controller.digital_read(self.__exit_btn_input)

        return state

    def __lock_mechanism_output_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if self.__lock_mechanism_output != register.value:
            self.__lock_mechanism_output = register.value

    def __set_lock_mechanism_1(self, value=0):

        if self.__controller.is_valid_gpio(self.__lock_mechanism_output):
            self.__controller.digital_write(self.__lock_mechanism_output, value)

    def __time_to_open_cb(self, register):

        if not register.is_int_or_float():
            # self._log_bad_value_register(self.__logger, register)
            return

        if self.__open_timer.expiration_time != register.value:
            self.__open_timer.expiration_time = register.value

    def __door_closed_state(self):

        state = False

        if self.__controller.is_valid_gpio(self.__door_closed_input):
            state = self.__controller.digital_read(self.__door_closed_input)

        return state

    def __door_closed_input_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if self.__door_closed_input != register.value:
            self.__door_closed_input = register.value

    def __pir_state(self):

        state = False

        if self.__controller.is_valid_gpio(self.__pir_input):
            state = self.__controller.digital_read(self.__pir_input)

        return state

    def __pir_input_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if self.__pir_input != register.value:
            self.__pir_input = register.value

    def __window_closed_state(self):

        state = False

        if self.__controller.is_valid_gpio(self.__win_closed_input):
            state = self.__controller.digital_read(self.__win_closed_input)

        return state

    def __win_closed_input_cb(self, register):

        # Check data type.
        if not register.is_str():
            # self._log_bad_value_register(self.__logger, register)
            return

        if self.__win_closed_input != register.value:
            self.__win_closed_input = register.value

#endregion

#region Public Methods

    def init(self):

        self.__key = "ac"
        self.__name = "Security Zone {}".format(self.__identifier)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.__name))

        # Open timer 1.
        self.__open_timer = Timer(10)

        # Entry reader.
        entry_reader = self.__registers.by_name("{}.entry_reader_{}.enabled".format(self.__key, self.__identifier))
        if entry_reader is not None:
            entry_reader.update_handler = self.__entry_reader_cb

        # Exit reader.
        exit_reader = self.__registers.by_name("{}.exit_reader_{}.enabled".format(self.__key, self.__identifier))
        if exit_reader is not None:
            exit_reader.update_handler = self.__exit_reader_cb

        # Create exit button.
        exit_button_input = self.__registers.by_name("{}.exit_button_{}.input".format(self.__key, self.__identifier))
        if exit_button_input is not None:
            exit_button_input.update_handler = self.__exit_btn_input_cb

        # Create locking mechanism.
        lock_mechanism_output = self.__registers.by_name("{}.lock_mechanism_{}.output".format(self.__key, self.__identifier))
        if lock_mechanism_output is not None:
            lock_mechanism_output.update_handler = self.__lock_mechanism_output_cb

        # Get time to open the latch.
        time_to_open = self.__registers.by_name("{}.time_to_open_{}".format(self.__key, self.__identifier))
        if time_to_open is not None:
            time_to_open.update_handler = self.__time_to_open_cb

        # Door closed 1
        door_closed_input = self.__registers.by_name("{}.door_closed_{}.input".format(self.__key, self.__identifier))
        if door_closed_input is not None:
            door_closed_input.update_handler = self.__door_closed_input_cb

        # PIR 1
        pir_input = self.__registers.by_name("{}.pir_{}.input".format(self.__key, self.__identifier))
        if pir_input is not None:
            pir_input.update_handler = self.__pir_input_cb

        # Window Closed 1
        win_closed_input = self.__registers.by_name("{}.window_closed_{}.input".format(self.__key, self.__identifier))
        if win_closed_input is not None:
            win_closed_input.update_handler = self.__win_closed_input_cb

    def update(self):

        # Check entry card reader.
        if self.__entry_reader is not None:

            # Update card reader.
            self.__entry_reader.update()

            if self.__entry_reader.reader_state == ReaderState.STOP:
                self.__logger.warning("Card reader {}; State {}; Port {}."\
                    .format(self.__entry_reader.reader_id, \
                            self.__entry_reader.reader_state, \
                            self.__entry_reader.port_name))

                self.__entry_reader.start()

            if self.__entry_reader.reader_state == ReaderState.NONE:
                self.__logger.warning("Card reader {}; State {}."\
                    .format(self.__entry_reader.reader_id, self.__entry_reader.reader_state))

                self.__entry_reader.start()

        # Check the exit card reader.
        if self.__exit_reader is not None:

            # Update card reader.
            self.__exit_reader.update()

            if self.__exit_reader.reader_state == ReaderState.STOP:
                self.__logger.warning("Card reader {}; State {}; Port {}."\
                    .format(self.__exit_reader.reader_id, \
                            self.__exit_reader.reader_state, \
                            self.__exit_reader.port_name))

                self.__exit_reader.start()

            if self.__exit_reader.reader_state == ReaderState.NONE:
                self.__logger.warning("Card reader {}; State {}."\
                    .format(self.__exit_reader.reader_id, self.__exit_reader.reader_state))

                self.__exit_reader.start()

        # Check if the button is pressed.
        btn_value = self.__exit_btn_state()
        if btn_value == 1:
            if self.__open_door_flag == 0:
                self.__open_door_flag = 1

        # Check if the flag is raise.
        if self.__open_door_flag == 1:
            self.__set_lock_mechanism_1(1)
            self.__open_timer.update_last_time()
            self.__open_door_flag = 0
            self.__free_to_lock = 1

        # Check is it time to close the latch.
        if self.__open_door_flag == 0:
            self.__open_timer.update()

            if self.__open_timer.expired:
                self.__open_timer.clear()

                if self.__free_to_lock == 1:
                    self.__set_lock_mechanism_1(0)
                    self.__free_to_lock = 0

        # Read input flag of the door.
        door_closed_state = self.__registers.by_name("{}.door_closed.state_{}".format(self.__key, self.__identifier))
        if door_closed_state is not None:
            door_closed_state.value = self.__door_closed_state()

        # PIR 1
        pir_state = self.__registers.by_name("{}.pir.state_{}".format(self.__key, self.__identifier))
        if pir_state is not None:
            pir_state.value = self.__pir_state()

        # Window Closed 1
        window_closed_state = self.__registers.by_name("{}.window_closed.state_{}".format(self.__key, self.__identifier))
        if window_closed_state is not None:
            window_closed_state.value = self.__window_closed_state()

    def shutdown(self):

        self.__set_lock_mechanism_1(0)

        # Destroy the cardreader.
        if self.__entry_reader is not None:
            self.__entry_reader.stop()

            while self.__entry_reader.reader_state == ReaderState.RUN:
                pass

        if self.__exit_reader is not None:
            self.__exit_reader.stop()

            while self.__exit_reader.reader_state == ReaderState.RUN:
                pass

    def set_reader_read(self, cb):

        if cb is None:
            return

        self.__reader_read_cb = cb

    def add_allowed_attendant(self, card_id):
        """Add allowed attendant ID.

        Parameters
        ----------
        ids : str
            Cards id.

        """

        if card_id is None:
            return

        if card_id == "":
            return

        if card_id in self.__allowed_attendant:
            pass

        else:
            self.__allowed_attendant.append(card_id)

    def add_allowed_attendees(self, ids):
        """Add allowed attendees IDs.

        Parameters
        ----------
        ids : array
            Cards id.

        """

        if ids is None:
            return

        self.__allowed_attendant.clear()

        for card_id in ids:
            self.add_allowed_attendant(card_id)

#endregion
