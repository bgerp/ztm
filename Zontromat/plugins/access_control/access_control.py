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
from utils.circular_buffer import CircularBuffer

from plugins.base_plugin import BasePlugin

from devices.TERACOM.act230 import ACT230
from devices.TERACOM.act230 import ReaderState

from data import verbal_const

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

class RegistrarState(Enum):
    """Registrar state enumeration class."""

    GetFromQue = 1
    Send = 2

class AccessControl(BasePlugin):
    """Access control and security."""

#region Attributes

    __logger = None
    """Logger"""

    __allowed_attendant = []
    """Allowed attendant"""

    __last_30_attendees = None
    """Last 30 attendees"""

    __attendees_queue = None
    """Register queue."""

    __cards_queue_size = 10000
    """Uplink queue size."""

    __registrar_state = None
    """Registrar state."""

    __first_queue_record = None
    """Firs record."""

    __is_empty_timer = None
    """Is empty timer."""



    __entry_reader_1 = None
    """Entry card reader 1."""

    __exit_reader_1 = None
    """Exit card reader 1."""

    __exit_btn_1_input =  verbal_const.OFF # "DI0"
    """Exit button input 1."""

    __lock_mechanism_1_output =  verbal_const.OFF # "DO0"
    """Locking mechanism 1 output."""

    __door_1_closed_input =  verbal_const.OFF # "DI2"
    """Door 1 closed input."""

    __free_to_lock_1 = 0
    """Free to lock 1 flag."""

    __open_door_1_flag = 0
    """Open door 1 flag."""

    __open_timer_1 = None
    """Open timer 1."""

    __pir_1_input = verbal_const.OFF # "DI0"
    """PIR 1"""

    __win_1_closed_input = verbal_const.OFF # "DI3"
    """Window closed sensor 1"""


    __entry_reader_2 = None
    """Entry reader 2"""

    __exit_reader_2 = None
    """Exit reader 2"""

    __exit_btn_2_input =  verbal_const.OFF # "DI0"
    """Exit button input 2."""

    __lock_mechanism_2_output =  verbal_const.OFF # "DO0"
    """Locking mechanism 2 output."""

    __door_2_closed_input = verbal_const.OFF # "DI2"
    """Door 2 closed input."""

    __free_to_lock_2 = 0
    """Free to lock 2 flag."""

    __open_door_2_flag = 0
    """Open door 2 flag."""

    __open_timer_2 = None
    """Open timer 2"""

    __pir_2_input = verbal_const.OFF # "DI0"
    """PIR 2"""

    __win_2_closed_input = verbal_const.OFF # "DI3"
    """Window closed sensor 2"""

#endregion

#region Destructor

    def __del__(self):

        del self.__logger
        del self.__allowed_attendant
        del self.__last_30_attendees
        del self.__attendees_queue
        del self.__cards_queue_size
        del self.__registrar_state
        del self.__first_queue_record

        del self.__entry_reader_1
        del self.__exit_reader_1
        del self.__exit_btn_1_input
        del self.__lock_mechanism_1_output
        del self.__door_1_closed_input
        del self.__free_to_lock_1
        del self.__open_door_1_flag
        del self.__open_timer_1

        del self.__entry_reader_2
        del self.__exit_reader_2
        del self.__exit_btn_2_input
        del self.__lock_mechanism_2_output
        del self.__door_1_closed_input
        del self.__free_to_lock_2
        del self.__open_door_2_flag
        del self.__open_timer_2

#endregion

#region Private Methods

    def __is_allowed(self, card_id):

        allowed = False

        for card in self.__allowed_attendant:
            if card["card_id"] == card_id:
                allowed = True
                break

        return allowed

    def __add_allowed_attendant(self, card_id):
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

    def __add_allowed_attendees(self, ids):
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
            self.__add_allowed_attendant(card_id)

    def __allowed_attendees_cb(self, register):

        self.__add_allowed_attendees(register.value)


    def __is_empty_timeout_cb(self, register):

        self.__is_empty_timer.expiration_time = register.value

    def __set_zone_occupied(self, flag):

        is_empty = self._registers.by_name(self._key + ".zone_occupied")
        if is_empty is not None:
            is_empty.value = flag

        is_empty = self._registers.by_name("env.is_empty")
        if is_empty is not None:
            is_empty.value = flag

    def __update_occupation(self):

        pir_1 = self.__pir_1_state()
        pir_2 = self.__pir_2_state()
        door_1_closed_state = self.__door_1_closed_state()
        door_2_closed_state = self.__door_2_closed_state()

        occupation_state = (pir_1 or pir_2 or door_1_closed_state or door_2_closed_state)

        # Clear time interval.
        if occupation_state:
            self.__is_empty_timer.update_last_time()
            self.__set_zone_occupied(1)

        # Update is empty timer.
        self.__is_empty_timer.update()

        if self.__is_empty_timer.expired:
            self.__is_empty_timer.clear()

            self.__set_zone_occupied(0)

#endregion

#region Under Construction

    def __reader_read(self, card_id, reader_id):

        # Set flag to open the door.
        if self.__is_allowed(card_id):
            if self.__open_door_1_flag == 0:
                self.__open_door_1_flag = 1

        # Create a record.
        record = { \
            "ts": time.time(), \
            "card_id": card_id, \
            "reader_id": reader_id, \
        }

        # Check the queue and take action.
        if self.__attendees_queue.full():
            self.__logger.warning("The queue is full.")
        else:
            self.__logger.debug("Received ID: {}".format(record))
            self.__attendees_queue.put(record)
            self.__last_30_attendees.put(record)


    def __entry_reader_1_cb(self, register):

        if register.value == verbal_const.YES and self.__entry_reader_1 is None:
            key = register.base_name
            card_reader_vendor = self._registers.by_name(key + ".entry_reader.vendor").value
            card_reader_model = self._registers.by_name(key + ".entry_reader.model").value
            card_reader_serial_number = self._registers.by_name(key + ".entry_reader.serial_number").value
            card_reader_port_name = self._registers.by_name(key + ".entry_reader.port.name").value
            card_reader_port_baudrate = self._registers.by_name(key + ".entry_reader.port.baudrate").value

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
                    self.__entry_reader_1 = ACT230(reader_config)
                    if self.__entry_reader_1.reader_state is ReaderState.NONE:
                        self.__entry_reader_1.cb_read_card(self.__reader_read)
                        self.__entry_reader_1.start()

        elif register.value == verbal_const.NO and self.__entry_reader_1 is not None:
            self.__entry_reader_1.stop()

            while self.__entry_reader_1.reader_state == ReaderState.RUN:
                pass

            del self.__entry_reader_1

    def __exit_reader_1_cb(self, register):

        if register.value == verbal_const.YES and self.__exit_reader_1 is None:
            key = register.base_name
            card_reader_vendor = self._registers.by_name(key + ".exit_reader.vendor").value
            card_reader_model = self._registers.by_name(key + ".exit_reader.model").value
            card_reader_serial_number = self._registers.by_name(key + ".exit_reader.serial_number").value
            card_reader_port_name = self._registers.by_name(key + ".exit_reader.port.name").value
            card_reader_port_baudrate = self._registers.by_name(key + ".exit_reader.port.baudrate").value

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
                    self.__exit_reader_1 = ACT230(reader_config)
                    if self.__exit_reader_1.reader_state is ReaderState.NONE:
                        self.__exit_reader_1.cb_read_card(self.__reader_read)
                        self.__exit_reader_1.start()

        elif register.value == verbal_const.NO and self.__exit_reader_1 is not None:
            self.__exit_reader_1.stop()

            while self.__exit_reader_1.reader_state == ReaderState.RUN:
                pass

            del self.__exit_reader_1

    def __exit_btn_1_input_cb(self, register):

            self.__exit_button_input = register.value

    def __exit_btn_1_state(self):

        state = 0

        if self.__exit_button_input != verbal_const.OFF and self.__exit_button_input != "":
            state = self._controller.digital_read(self.__exit_button_input)

        return state

    def __lock_mechanism_1_output_cb(self, register):

        self.__lock_mechanism_output = register.value

    def __set_lock_mechanism_1(self, value=0):

        if self.__lock_mechanism_output != verbal_const.OFF:
            self._controller.digital_write(self.__lock_mechanism_output, value)

    def __time_to_open_1_cb(self, register):

        self.__open_timer_1.expiration_time = register.value

    def __door_1_closed_state(self):

        state = 0

        if self.__door_1_closed_input != verbal_const.OFF and self.__door_1_closed_input != "":
            state = self._controller.digital_read(self.__door_1_closed_input)

        return state

    def __door_1_closed_input_cb(self, register):

        self.__door_1_closed_input = register.value

    def __pir_1_state(self):

        state = 0

        if self.__pir_1_input != verbal_const.OFF and self.__pir_1_input != "":
            state = self._controller.digital_read(self.__pir_1_input)

        return state

    def __pir_1_input_cb(self, register):

        self.__pir_1_input = register.value

    def __window_1_closed_state(self):

        state = 0

        if self.__win_1_closed_input != verbal_const.OFF and self.__win_1_closed_input != "":
            state = self._controller.digital_read(self.__win_1_closed_input)

        return state

    def __win_1_closed_input_cb(self, register):

        self.__win_1_closed_input = register.value

    def __init_block_1(self):

        # Open timer 1.
        self.__open_timer_1 = Timer(10)

        # Entry reader.
        entry_reader = self._registers.by_name(self._key + ".entry_reader.enabled")
        if entry_reader is not None:
            entry_reader.update_handler = self.__entry_reader_1_cb

        # Exit reader.
        exit_reader = self._registers.by_name(self._key + ".exit_reader.enabled")
        if exit_reader is not None:
            exit_reader.update_handler = self.__exit_reader_1_cb

        # Create exit button.
        exit_button_input = self._registers.by_name(self._key + ".exit_button.input")
        if exit_button_input is not None:
            exit_button_input.update_handler = self.__exit_btn_1_input_cb

        # Create locking mechanism.
        lock_mechanism_output = self._registers.by_name(self._key + ".lock_mechanism.output")
        if lock_mechanism_output is not None:
            lock_mechanism_output.update_handler = self.__lock_mechanism_1_output_cb

        # Get time to open the latch.
        time_to_open = self._registers.by_name(self._key + ".time_to_open")
        if time_to_open is not None:
            time_to_open.update_handler = self.__time_to_open_1_cb

        # Door closed 1
        door_closed_input = self._registers.by_name(self._key + ".door_closed.input")
        if door_closed_input is not None:
            door_closed_input.update_handler = self.__door_1_closed_input_cb

        # PIR 1
        pir_input = self._registers.by_name(self._key + ".pir.input")
        if pir_input is not None:
            pir_input.update_handler = self.__pir_1_input_cb

        # Window Closed 1
        win_closed_input = self._registers.by_name(self._key + ".window_closed.input")
        if win_closed_input is not None:
            win_closed_input.update_handler = self.__win_1_closed_input_cb

    def __update_block_1(self):

        # Check entry card reader.
        if self.__entry_reader_1 is not None:

            # Update card reader.
            self.__entry_reader_1.update()

            if self.__entry_reader_1.reader_state == ReaderState.STOP:
                self.__logger.warning("Card reader {}; State {}; Port {}."\
                    .format(self.__entry_reader_1.reader_id, \
                            self.__entry_reader_1.reader_state, \
                            self.__entry_reader_1.port_name))

                self.__entry_reader_1.start()

            if self.__entry_reader_1.reader_state == ReaderState.NONE:
                self.__logger.warning("Card reader {}; State {}."\
                    .format(self.__entry_reader_1.reader_id, self.__entry_reader_1.reader_state))

                self.__entry_reader_1.start()

        # Check the exit card reader.
        if self.__exit_reader_1 is not None:

            # Update card reader.
            self.__exit_reader_1.update()

            if self.__exit_reader_1.reader_state == ReaderState.STOP:
                self.__logger.warning("Card reader {}; State {}; Port {}."\
                    .format(self.__exit_reader_1.reader_id, \
                            self.__exit_reader_1.reader_state, \
                            self.__exit_reader_1.port_name))

                self.__exit_reader_1.start()

            if self.__exit_reader_1.reader_state == ReaderState.NONE:
                self.__logger.warning("Card reader {}; State {}."\
                    .format(self.__exit_reader_1.reader_id, self.__exit_reader_1.reader_state))

                self.__exit_reader_1.start()

        # Check if the button is pressed.
        btn_value = self.__exit_btn_1_state()
        if btn_value == 1:
            if self.__open_door_1_flag == 0:
                self.__open_door_1_flag = 1

        # Check if the flag is raise.
        if self.__open_door_1_flag == 1:
            self.__set_lock_mechanism_1(1)
            self.__open_timer_1.update_last_time()
            self.__open_door_1_flag = 0
            self.__free_to_lock_1 = 1

        # Check is it time to close the latch.
        if self.__open_door_1_flag == 0:
            self.__open_timer_1.update()

            if self.__open_timer_1.expired:
                self.__open_timer_1.clear()

                if self.__free_to_lock_1 == 1:
                    self.__set_lock_mechanism_1(0)
                    self.__free_to_lock_1 = 0

        # Read input flag of the door.
        door_closed_state = self._registers.by_name(self._key + ".door_closed.state")
        if door_closed_state is not None:
            door_closed_state.value = self.__door_1_closed_state()

        # PIR 1
        pir_state = self._registers.by_name(self._key + ".pir.state")
        if pir_state is not None:
            pir_state.value = self.__pir_1_state()

        # Window Closed 1
        window_closed_state = self._registers.by_name(self._key + ".window_closed.state")
        if window_closed_state is not None:
            window_closed_state.value = self.__window_1_closed_state()

    def __shutdown_block_1(self):

        self.__set_lock_mechanism_1(0)

        # Destroy the cardreader.
        if self.__entry_reader_1 is not None:
            self.__entry_reader_1.stop()

            while self.__entry_reader_1.reader_state == ReaderState.RUN:
                pass

        if self.__exit_reader_1 is not None:
            self.__exit_reader_1.stop()

            while self.__exit_reader_1.reader_state == ReaderState.RUN:
                pass


    def __entry_reader_2_cb(self, register):

        if register.value == verbal_const.YES and self.__entry_reader_2 is None:
            key = register.base_name
            card_reader_vendor = self._registers.by_name(key + ".entry_reader2.vendor").value
            card_reader_model = self._registers.by_name(key + ".entry_reader2.model").value
            card_reader_serial_number = self._registers.by_name(key + ".entry_reader2.serial_number").value
            card_reader_port_name = self._registers.by_name(key + ".entry_reader2.port.name").value
            card_reader_port_baudrate = self._registers.by_name(key + ".entry_reader2.port.baudrate").value

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
                    self.__entry_reader_2 = ACT230(reader_config)
                    if self.__entry_reader_2.reader_state is ReaderState.NONE:
                        self.__entry_reader_2.cb_read_card(self.__reader_read)
                        self.__entry_reader_2.start()

        elif register.value == verbal_const.NO and self.__entry_reader_2 is not None:
            self.__entry_reader_2.stop()

            while self.__entry_reader_2.reader_state == ReaderState.RUN:
                pass

            del self.__entry_reader_2

    def __exit_reader_2_cb(self, register):

        if register.value == verbal_const.YES and self.__exit_reader_2 is None:
            key = register.base_name
            card_reader_vendor = self._registers.by_name(key + ".exit_reader2.vendor").value
            card_reader_model = self._registers.by_name(key + ".exit_reader2.model").value
            card_reader_serial_number = self._registers.by_name(key + ".exit_reader2.serial_number").value
            card_reader_port_name = self._registers.by_name(key + ".exit_reader2.port.name").value
            card_reader_port_baudrate = self._registers.by_name(key + ".exit_reader2.port.baudrate").value

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
                    self.__exit_reader_2 = ACT230(reader_config)
                    if self.__exit_reader_2.reader_state is ReaderState.NONE:
                        self.__exit_reader_2.cb_read_card(self.__reader_read)
                        self.__exit_reader_2.start()

        elif register.value == verbal_const.NO and self.__exit_reader_2 is not None:
            self.__exit_reader_2.stop()

            while self.__exit_reader_2.reader_state == ReaderState.RUN:
                pass

            del self.__exit_reader_2

    def __exit_btn_2_input_cb(self, register):

            self.__exit_button2_input = register.value

    def __exit_btn_2_state(self):

        state = 0

        if self.__exit_button2_input != verbal_const.OFF and self.__exit_button2_input != "":
            state = self._controller.digital_read(self.__exit_button2_input)

        return state

    def __lock_mechanism_2_output_cb(self, register):

        self.__lock_mechanism2_output = register.value

    def __set_lock_mechanism_2(self, value=0):

        if self.__lock_mechanism2_output != verbal_const.OFF:
            self._controller.digital_write(self.__lock_mechanism2_output, value)

    def __time_to_open_2_cb(self, register):

        self.__open_timer_2.expiration_time = register.value

    def __door_2_closed_state(self):

        state = 0

        if self.__door_closed_2_input != verbal_const.OFF and self.__door_closed_2_input != "":
            state = self._controller.digital_read(self.__door_closed_2_input)

        return state

    def __door_2_closed_input_cb(self, register):

        self.__door_closed_2_input = register.value

    def __pir_2_input_cb(self, register):

        self.__pir_2_input = register.value

    def __pir_2_state(self):
        
        state = 0

        if self.__pir_2_input != verbal_const.OFF and self.__pir_2_input != "":
            state = self._controller.digital_read(self.__pir_2_input)

        return state

    def __win_2_closed_input_cb(self, register):

        self.__win_2_closed_input = register.value

    def __window_2_closed_state(self):

        state = 0

        if self.__win_2_closed_input != verbal_const.OFF and self.__win_2_closed_input != "":
            state = self._controller.digital_read(self.__win_2_closed_input)

        return state

    def __init_block_2(self):

        self.__open_timer_2 = Timer(10)

        # Entry reader.
        entry_reader2 = self._registers.by_name(self._key + ".entry_reader2.enabled")
        if entry_reader2 is not None:
            entry_reader2.update_handler = self.__entry_reader_2_cb

        # Exit reader.
        exit_reader = self._registers.by_name(self._key + ".exit_reader2.enabled")
        if exit_reader is not None:
            exit_reader.update_handler = self.__exit_reader_2_cb

        # Create exit button.
        exit_button_input = self._registers.by_name(self._key + ".exit_button2.input")
        if exit_button_input is not None:
            exit_button_input.update_handler = self.__exit_btn_2_input_cb

        # Create locking mechanism.
        lock_mechanism_output = self._registers.by_name(self._key + ".lock_mechanism2.output")
        if lock_mechanism_output is not None:
            lock_mechanism_output.update_handler = self.__lock_mechanism_2_output_cb

        # Get time to open the latch.
        time_to_open = self._registers.by_name(self._key + ".time_to_open2")
        if time_to_open is not None:
            time_to_open.update_handler = self.__time_to_open_2_cb

        door_closed_input = self._registers.by_name(self._key + ".door_closed2.input")
        if door_closed_input is not None:
            door_closed_input.update_handler = self.__door_2_closed_input_cb

        # PIR 2
        pir_input = self._registers.by_name(self._key + ".pir2.input")
        if pir_input is not None:
            pir_input.update_handler = self.__pir_2_input_cb

        # Window Closed 2
        win_closed_input = self._registers.by_name(self._key + ".window_closed2.input")
        if win_closed_input is not None:
            win_closed_input.update_handler = self.__win_2_closed_input_cb

    def __update_block_2(self):

        # Check entry card reader.
        if self.__entry_reader_2 is not None:

            # Update card reader.
            self.__entry_reader_2.update()

            if self.__entry_reader_2.reader_state == ReaderState.STOP:
                self.__logger.warning("Card reader {}; State {}; Port {}."\
                    .format(self.__entry_reader_2.reader_id, \
                            self.__entry_reader_2.reader_state, \
                            self.__entry_reader_2.port_name))

                self.__entry_reader_2.start()

            if self.__entry_reader_2.reader_state == ReaderState.NONE:
                self.__logger.warning("Card reader {}; State {}."\
                    .format(self.__entry_reader_2.reader_id, self.__entry_reader_2.reader_state))

                self.__entry_reader_2.start()

        # Check the exit card reader.
        if self.__exit_reader_2 is not None:

            # Update card reader.
            self.__exit_reader_2.update()

            if self.__exit_reader_2.reader_state == ReaderState.STOP:
                self.__logger.warning("Card reader {}; State {}; Port {}."\
                    .format(self.__exit_reader_2.reader_id, \
                            self.__exit_reader_2.reader_state, \
                            self.__exit_reader_2.port_name))

                self.__exit_reader_2.start()

            if self.__exit_reader_2.reader_state == ReaderState.NONE:
                self.__logger.warning("Card reader {}; State {}."\
                    .format(self.__exit_reader_2.reader_id, self.__exit_reader_2.reader_state))

                self.__exit_reader_2.start()

        # Check if the button is pressed.
        btn_value = self.__exit_btn_2_state()
        if btn_value == 1:
            if self.__open_door_2_flag == 0:
                self.__open_door_2_flag = 1

        # Check if the flag is raise.
        if self.__open_door_2_flag == 1:
            self.__set_lock_mechanism_2(1)
            self.__open_timer_2.update_last_time()
            self.__open_door_2_flag = 0
            self.__free_to_lock_2 = 1

        # Check is it time to close the latch.
        if self.__open_door_2_flag == 0:
            self.__open_timer_2.update()

            if self.__open_timer_2.expired:
                self.__open_timer_2.clear()

                if self.__free_to_lock_2 == 1:
                    self.__set_lock_mechanism_2(0)
                    self.__free_to_lock_2 = 0

        # Read input flag of the door.
        door_closed_state = self._registers.by_name(self._key + ".door_closed2.state")
        if door_closed_state is not None:
            door_closed_state.value = self.__door_2_closed_state()

        # PIR 2
        pir_state = self._registers.by_name(self._key + ".pir2.state")
        if pir_state is not None:
            pir_state.value = self.__pir_2_state()

        # Window Closed 2
        window_closed_state = self._registers.by_name(self._key + ".window_closed2.state")
        if window_closed_state is not None:
            window_closed_state.value = self.__window_2_closed_state()

    def __shutdown_block_2(self):

        self.__set_lock_mechanism_2(0)

        # Destroy the cardreader.
        if self.__entry_reader_2 is not None:
            self.__entry_reader_2.stop()

            while self.__entry_reader_2.reader_state == ReaderState.RUN:
                pass

        if self.__exit_reader_2 is not None:
            self.__exit_reader_2.stop()

            while self.__exit_reader_2.reader_state == ReaderState.RUN:
                pass

#endregion

#region Public Methods

    def init(self):

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Create last 30 attendees.
        self.__last_30_attendees = CircularBuffer(30)

        # Create queue for the card.
        self.__attendees_queue = queue.Queue(self.__cards_queue_size)

        # Set registrar state.
        self.__registrar_state = StateMachine(RegistrarState.GetFromQue)

        # Card reader allowed IDs.
        allowed_attendees = self._registers.by_name(self._key + ".allowed_attendees")
        if allowed_attendees is not None:
            allowed_attendees.update_handler = self.__allowed_attendees_cb

        # Is empty timer.
        self.__is_empty_timer = Timer(3600)

        # Is empty timeout.
        is_empty_timeout = self._registers.by_name("env.is_empty_timeout")
        if is_empty_timeout is not None:
            is_empty_timeout.update_handler = self.__is_empty_timeout_cb

        self.__init_block_1()

        self.__init_block_2()

    def update(self):

        self.__update_block_1()

        self.__update_block_2()

        # If the queue is not empty,
        # take first and send it to the ERP service.
        if self.__attendees_queue.empty() is not True:

            if self.__registrar_state.is_state(RegistrarState.GetFromQue):
                self.__first_queue_record = self.__attendees_queue.get()
                self.__registrar_state.set_state(RegistrarState.Send)

            if self.__registrar_state.is_state(RegistrarState.Send):
                # Send event to the ERP service.
                rec = [self.__first_queue_record]
                successful = self._erp_service.sync(rec)

                if successful is not None:
                    self.__logger.debug("Send ID: {}".format(self.__first_queue_record))
                    self.__registrar_state.set_state(RegistrarState.GetFromQue)

        self.__update_occupation()

        # Update last 30 attendees in list.
        last30_attendees = self._registers.by_name(self._key + ".last30_attendees")
        if last30_attendees is not None:
            str_data = str(self.__last_30_attendees)
            last30_attendees.value = str_data


    def shutdown(self):
        """Shutting down the reader."""

        self.__logger.info("Shutting down the {}".format(self.name))

        self.__shutdown_block_1()

        self.__shutdown_block_2()

#endregion
