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

from plugins.base_plugin import BasePlugin

from utils.logger import get_logger
from utils.timer import Timer

from data import verbal_const

from devices.utils.card_readers.card_reader_factory import CardReaderFactory
from devices.utils.card_readers.card_reader_state import CardReaderState

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

    __identifier = 0
    """Security zone identifier."""

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

    __free_to_lock = 0
    """Free to lock flag."""

    __open_door_flag = 0
    """Open door flag."""

    __open_timer = None
    """Open timer."""

    __reader_read_cb = None
    """Reader read callback"""

    __door_window_blind_output = verbal_const.OFF

#endregion

#region Constructor / Destructor

    def __init__(self, **kwargs):
        """Constructor"""

        super().__init__(kwargs)

        if "identifier" in kwargs:
            self.__identifier = kwargs["identifier"]

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

    def __reader_read(self, card_id, serial_number):

        # Set flag to open the door.
        if self.__is_allowed(card_id):
            if self.__open_door_flag == 0:
                self.__open_door_flag = 1

        if self.__reader_read_cb is not None:
            self.__reader_read_cb(card_id, serial_number)

    def __entry_reader_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != "" and self.__entry_reader is None:

            key = register.base_name

            params = register.value.split("/")

            vendor = params[0]
            model = params[1]
            serial_number = params[2]

            register = self._registers.by_name("{}.entry_reader_{}.port.name"\
                .format(key, self.__identifier))

            if "ac.entry_reader_1.port.name" == register.name:
                register.value = "usb:072f:2200"

            port_name = register.value

            baudrate = self._registers.by_name("{}.entry_reader_{}.port.baudrate"\
                .format(key, self.__identifier)).value


            # Create the card reader.
            self.__entry_reader = CardReaderFactory.create(\
                vendor=vendor,\
                model=model,\
                serial_number=serial_number,\
                port_name=port_name,\
                baudrate=baudrate)

            # Check if it is working.
            if self.__entry_reader is not None:
                if self.__entry_reader.reader_state == CardReaderState.NONE:
                    self.__entry_reader.cb_read_card(self.__reader_read)
                    self.__entry_reader.init()

        elif register.value == verbal_const.OFF and self.__entry_reader is not None:
            self.__entry_reader.shutdown()

            while self.__entry_reader.reader_state == CardReaderState.RUN:
                pass

            del self.__entry_reader

    def __exit_reader_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != "" and self.__exit_reader is None:

            key = register.base_name

            params = register.value.split("/")

            vendor = params[0]
            model = params[1]
            serial_number = params[2]

            port_name = self._registers.by_name("{}.exit_reader_{}.port.name"\
                .format(key, self.__identifier)).value

            baudrate = self._registers.by_name("{}.exit_reader_{}.port.baudrate"\
                .format(key, self.__identifier)).value

            # Create the card reader.
            self.__exit_reader = CardReaderFactory.create(\
                vendor=vendor,\
                model=model,\
                serial_number=serial_number,\
                port_name=port_name,\
                baudrate=baudrate)

            # Check if it is working.
            if self.__exit_reader is not None:
                if self.__exit_reader.reader_state == CardReaderState.NONE:
                    self.__exit_reader.cb_read_card(self.__reader_read)
                    self.__exit_reader.init()

        elif register.value == verbal_const.OFF and self.__exit_reader is not None:
            self.__exit_reader.shutdown()

            while self.__exit_reader.reader_state == CardReaderState.RUN:
                pass

            del self.__exit_reader

    def __exit_btn_input_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__exit_btn_input != register.value:
            self.__exit_btn_input = register.value

    def __exit_btn_state(self):

        state = False

        if self._controller.is_valid_gpio(self.__exit_btn_input):
            state = self._controller.digital_read(self.__exit_btn_input)

        return state

    def __lock_mechanism_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__lock_mechanism_output != register.value:
            self.__lock_mechanism_output = register.value

    def __set_lock_mechanism(self, value=0):

        if self._controller.is_valid_gpio(self.__lock_mechanism_output):
            self._controller.digital_write(self.__lock_mechanism_output, value)

    def __time_to_open_cb(self, register):

        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__open_timer.expiration_time != register.value:
            self.__open_timer.expiration_time = register.value

    def __door_window_blind_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__door_window_blind_output != register.value:
            self.__door_window_blind_output = register.value

    def __door_window_blind_value_cb(self, register):

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value == 0 or register.value == 1:
            self.__set_door_window_blind(register.value)

    def __set_door_window_blind(self, value=0):

        if self._controller.is_valid_gpio(self.__door_window_blind_output):
            self._controller.digital_write(self.__door_window_blind_output, value)

#endregion

#region Public Methods

    def init(self):
        """Init"""

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Open timer 1.
        self.__open_timer = Timer(10)

        # Entry reader.
        entry_reader = self._registers.by_name("{}.entry_reader_{}.enabled".format(self._key, self.__identifier))
        if entry_reader is not None:
            entry_reader.update_handler = self.__entry_reader_cb

        # Exit reader.
        exit_reader = self._registers.by_name("{}.exit_reader_{}.enabled".format(self._key, self.__identifier))
        if exit_reader is not None:
            exit_reader.update_handler = self.__exit_reader_cb

        # Create exit button.
        exit_button_input = self._registers.by_name("{}.exit_button_{}.input".format(self._key, self.__identifier))
        if exit_button_input is not None:
            exit_button_input.update_handler = self.__exit_btn_input_cb

        # Create locking mechanism.
        lock_mechanism_output = self._registers.by_name("{}.lock_mechanism_{}.output".format(self._key, self.__identifier))
        if lock_mechanism_output is not None:
            lock_mechanism_output.update_handler = self.__lock_mechanism_output_cb

        # Get time to open the latch.
        time_to_open = self._registers.by_name("{}.time_to_open_{}".format(self._key, self.__identifier))
        if time_to_open is not None:
            time_to_open.update_handler = self.__time_to_open_cb

        # Door window blind.
        door_window_blind_output = self._registers.by_name("{}.door_window_blind_{}.output".format(self._key, self.__identifier))
        if door_window_blind_output is not None:
            door_window_blind_output.update_handler = self.__door_window_blind_output_cb

        # Door window blind.
        door_window_blind_value = self._registers.by_name("{}.door_window_blind_{}.value".format(self._key, self.__identifier))
        if door_window_blind_value is not None:
            door_window_blind_value.update_handler = self.__door_window_blind_value_cb

    def update(self):
        """Update"""

        # Check entry card reader.
        if self.__entry_reader is not None:

            # Update card reader.
            self.__entry_reader.update()

            if self.__entry_reader.reader_state == CardReaderState.STOP:

                message = "Card reader {}; State {}; Port {}."\
                    .format(self.__entry_reader.serial_number, \
                            self.__entry_reader.reader_state, \
                            self.__entry_reader.port_name)

                GlobalErrorHandler.log_cart_reader_stop(self.__logger, message)

                self.__entry_reader.init()

            if self.__entry_reader.reader_state == CardReaderState.NONE:

                message = "Card reader {}; State {}."\
                    .format(self.__entry_reader.serial_number, self.__entry_reader.reader_state)

                GlobalErrorHandler.log_cart_reader_none(self.__logger, message)

                self.__entry_reader.init()

        # Check the exit card reader.
        if self.__exit_reader is not None:

            # Update card reader.
            self.__exit_reader.update()

            if self.__exit_reader.reader_state == CardReaderState.STOP:

                message = "Card reader {}; State {}; Port {}."\
                    .format(self.__entry_reader.serial_number, \
                            self.__entry_reader.reader_state, \
                            self.__entry_reader.port_name)

                GlobalErrorHandler.log_cart_reader_stop(self.__logger, message)

                self.__exit_reader.init()

            if self.__exit_reader.reader_state == CardReaderState.NONE:

                message = "Card reader {}; State {}."\
                    .format(self.__entry_reader.serial_number, self.__entry_reader.reader_state)

                GlobalErrorHandler.log_cart_reader_none(self.__logger, message)

                self.__exit_reader.init()

        # Check if the button is pressed.
        btn_value = self.__exit_btn_state()
        if btn_value == 1:
            if self.__open_door_flag == 0:
                self.__open_door_flag = 1

        # Check if the flag is raise.
        if self.__open_door_flag == 1:
            self.__set_lock_mechanism(1)
            self.__set_door_window_blind(1)
            self.__open_timer.update_last_time()
            self.__open_door_flag = 0
            self.__free_to_lock = 1

        # Lock the door after when it is closed.
        door_closed = self._registers.by_name("ac.door_closed_1.input")
        if door_closed is not None:
            if self._controller.is_valid_gpio(door_closed.value):
                state = self._controller.digital_read(door_closed.value)
                if state == True:
                    if self.__free_to_lock == 1:
                        self.__set_lock_mechanism(0)
                        self.__set_door_window_blind(0)
                        self.__free_to_lock = 0

        # Check is it time to close the latch.
        if self.__open_door_flag == 0:

            self.__open_timer.update()
            if self.__open_timer.expired:
                self.__open_timer.clear()

                if self.__free_to_lock == 1:
                    self.__set_lock_mechanism(0)
                    self.__set_door_window_blind(0)
                    self.__free_to_lock = 0

    def shutdown(self):
        """Shutdown"""

        self.__set_lock_mechanism(0)
        self.__set_door_window_blind(0)

        # Destroy the cardreader.
        if self.__entry_reader is not None:
            self.__entry_reader.shutdown()

            while self.__entry_reader.reader_state == CardReaderState.RUN:
                pass

        if self.__exit_reader is not None:
            self.__exit_reader.shutdown()

            while self.__exit_reader.reader_state == CardReaderState.RUN:
                pass

    def set_reader_read(self, cb):
        """Set reader read calback."""

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
