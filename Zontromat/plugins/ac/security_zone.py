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

from plugins.base_plugin import BasePlugin

from utils.logger import get_logger
from utils.logic.timer import Timer

from data import verbal_const
from data.card_state import CardState

from devices.factories.card_readers.card_reader_factory import CardReaderFactory
from devices.factories.card_readers.card_reader_state import CardReaderState

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

class SecurityZone(BasePlugin):
    """Security zone definition class."""

#region Attribute

    __logger = None
    """Logger"""

    __identifier = 0
    """Security zone identifier."""

    __allowed_attendant = []
    """Allowed attendant."""

    __free_to_lock = 0
    """Free to lock flag."""

    __open_door_flag = 0
    """Open door flag."""


    __open_timer = None
    """Open timer."""

    __presence_timer = None
    """Presence timer"""


    __on_card_cb = None
    """Reader read callback"""


    __entry_reader = None
    """Entry card reader."""

    __exit_reader = None
    """Exit card reader."""

    __exit_btn_input = verbal_const.OFF # "DI0"
    """Exit button input."""

    __window_closed_input = verbal_const.OFF
    """Window closed sensor input."""

    __door_closed_input = verbal_const.OFF
    """Door closed sensor input."""

    __pir_input = verbal_const.OFF
    """PIR closed sensor input."""

    __lock_mechanism_output = verbal_const.OFF # "DO0"
    """Locking mechanism output."""

    __door_window_blind_output = verbal_const.OFF
    """Door window blind output."""

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        if "identifier" in config:
            self.__identifier = config["identifier"]

    def __del__(self):
        """Destructor"""

        if self.__entry_reader is not None:
            del self.__entry_reader

        if self.__exit_reader is not None:
            del self.__exit_reader

        if self.__open_timer is not None:
            del self.__open_timer

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (Registers)

    def __entry_reader_cb(self, register):

        # 1. Get data.
        valid_data = 0
        key = register.base_name
        reg_enabled = self._registers.by_name("{}.entry_reader_{}.enabled" .format(key, self.__identifier))
        reg_port_name = self._registers.by_name("{}.entry_reader_{}.port.name" .format(key, self.__identifier))
        reg_port_baudrate = self._registers.by_name("{}.entry_reader_{}.port.baudrate" .format(key, self.__identifier))

        # 2. If it is valid: delete old one.
        # Get settings.
        vendor = None
        model = None
        serial_number = None
        if reg_enabled is not None:
            if reg_enabled.data_type == "str":
                if reg_enabled.value == verbal_const.OFF:
                    self.__delete_reader(self.__entry_reader)
                    return # When fag is off. Just delete the object.

                elif reg_enabled.value != "":
                    params = reg_enabled.value.split("/")
                    vendor = params[0]
                    model = params[1]
                    serial_number = params[2]
                    valid_data += 1

                else:
                    GlobalErrorHandler.log_bad_register_value(self.__logger, reg_enabled)

            else:
                GlobalErrorHandler.log_bad_register_data_type(self.__logger, reg_enabled)

        else:
            GlobalErrorHandler.log_register_not_found(self.__logger,\
                "{}.entry_reader_{}.enabled" .format(key, self.__identifier))

        # Get port name.
        port_name = ""
        if reg_port_name is not None:
            if reg_port_name.data_type == "str":
                port_name = reg_port_name.value
                valid_data += 1
                # UNCOMMENT ONLY FOR TEST PURPOSE
                # if register.name == "ac.entry_reader_1.port.name":
                #     port_name = "usb:072f:2200

            else:
                GlobalErrorHandler.log_bad_register_data_type(self.__logger, reg_port_name)

        else:
            GlobalErrorHandler.log_register_not_found(self.__logger,\
                "{}.entry_reader_{}.port.name" .format(key, self.__identifier))


        # Get serial port baudrate.
        baudrate = 0
        if reg_port_baudrate is not None:
            if reg_port_baudrate.data_type == "int":
                if reg_port_baudrate.value > 0:
                    baudrate = reg_port_baudrate.value
                    valid_data += 1

                else:
                    GlobalErrorHandler.log_bad_register_value(self.__logger, reg_port_baudrate)

            else:
                GlobalErrorHandler.log_bad_register_data_type(self.__logger, reg_port_baudrate)

        else:
            GlobalErrorHandler.log_register_not_found(self.__logger,\
                "{}.entry_reader_{}.port.baudrate" .format(key, self.__identifier))

        # 3. Else: Pass
        if valid_data != 3:
            return

        # 2. If it is valid: delete old one.
        self.__delete_reader(self.__entry_reader)

        # 4. Create new one.
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
                self.__entry_reader.cb_read_card(self.__cb_read_card)
                self.__entry_reader.init()

    def __exit_reader_cb(self, register):

        # 1. Get data.
        valid_data = 0
        key = register.base_name
        reg_enabled = self._registers.by_name("{}.exit_reader_{}.enabled" .format(key, self.__identifier))
        reg_port_name = self._registers.by_name("{}.exit_reader_{}.port.name" .format(key, self.__identifier))
        reg_port_baudrate = self._registers.by_name("{}.exit_reader_{}.port.baudrate" .format(key, self.__identifier))

        # 2. If it is valid: delete old one.
        # Get settings.
        vendor = None
        model = None
        serial_number = None
        if reg_enabled is not None:
            if reg_enabled.data_type == "str":
                if reg_enabled.value == verbal_const.OFF:
                    self.__delete_reader(self.__exit_reader)
                    return # When fag is off. Just delete the object.

                elif reg_enabled.value != "":
                    params = reg_enabled.value.split("/")
                    vendor = params[0]
                    model = params[1]
                    serial_number = params[2]
                    valid_data += 1

                else:
                    GlobalErrorHandler.log_bad_register_value(self.__logger, reg_enabled)

            else:
                GlobalErrorHandler.log_bad_register_data_type(self.__logger, reg_enabled)

        else:
            GlobalErrorHandler.log_register_not_found(self.__logger,\
                "{}.exit_reader_{}.enabled" .format(key, self.__identifier))

        # Get port name.
        port_name = ""
        if reg_port_name is not None:
            if reg_port_name.data_type == "str":
                port_name = reg_port_name.value
                valid_data += 1
                # UNCOMMENT ONLY FOR TEST PURPOSE
                # if register.name == "ac.exit_reader_1.port.name":
                #     port_name = "usb:072f:2200

            else:
                GlobalErrorHandler.log_bad_register_data_type(self.__logger, reg_port_name)

        else:
            GlobalErrorHandler.log_register_not_found(self.__logger,\
                "{}.exit_reader_{}.port.name" .format(key, self.__identifier))


        # Get serial port baudrate.
        baudrate = 0
        if reg_port_baudrate is not None:
            if reg_port_baudrate.data_type == "int":
                if reg_port_baudrate.value > 0:
                    baudrate = reg_port_baudrate.value
                    valid_data += 1

                else:
                    GlobalErrorHandler.log_bad_register_value(self.__logger, reg_port_baudrate)

            else:
                GlobalErrorHandler.log_bad_register_data_type(self.__logger, reg_port_baudrate)

        else:
            GlobalErrorHandler.log_register_not_found(self.__logger,\
                "{}.exit_reader_{}.port.baudrate" .format(key, self.__identifier))

        # 3. Else: Pass
        if valid_data != 3:
            return

        # 2. If it is valid: delete old one.
        self.__delete_reader(self.__exit_reader)

        # 4. Create new one.
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
                self.__exit_reader.cb_read_card(self.__cb_read_card)
                self.__exit_reader.init()


    def __exit_btn_input_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__exit_btn_input = register.value

    def __window_closed_input_cb(self, register):

          # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__window_closed_input = register.value

    def __door_closed_input_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__door_closed_input = register.value

    def __pir_input_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__pir_input = register.value


    def __lock_mechanism_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__lock_mechanism_output = register.value

    def __door_window_blind_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__door_window_blind_output = register.value


    def __time_to_open_cb(self, register):

        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__open_timer.expiration_time = register.value

    def __is_empty_timeout_cb(self, register):

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__presence_timer.expiration_time = register.value

    def __door_window_blind_value_cb(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__set_door_window_blind(register.value)

    def __init_registers(self):

        # Get time to open the latch.
        time_to_open = self._registers.by_name("{}.time_to_open_{}".format(self.key, self.__identifier))
        if time_to_open is not None:
            time_to_open.update_handlers = self.__time_to_open_cb
            time_to_open.update()
    
        # Is empty timeout.
        is_empty_timeout = self._registers.by_name("envm.is_empty_timeout")
        if is_empty_timeout is not None:
            is_empty_timeout.update_handlers = self.__is_empty_timeout_cb
            is_empty_timeout.update()

        # Entry reader.
        entry_reader_enabled = self._registers.by_name("{}.entry_reader_{}.enabled".format(self.key, self.__identifier))
        if entry_reader_enabled is not None:
            entry_reader_enabled.update_handlers = self.__entry_reader_cb

        entry_reader_port_baudrate = self._registers.by_name("{}.entry_reader_{}.port.baudrate".format(self.key, self.__identifier))
        if entry_reader_port_baudrate is not None:
            entry_reader_port_baudrate.update_handlers = self.__entry_reader_cb

        entry_reader_port_name = self._registers.by_name("{}.entry_reader_{}.port.name".format(self.key, self.__identifier))
        if entry_reader_port_name is not None:
            entry_reader_port_name.update_handlers = self.__entry_reader_cb
            entry_reader_port_name.update()


        # Exit reader.
        exit_reader = self._registers.by_name("{}.exit_reader_{}.enabled".format(self.key, self.__identifier))
        if exit_reader is not None:
            exit_reader.update_handlers = self.__exit_reader_cb

        exit_reader_port_baudrate = self._registers.by_name("{}.exit_reader_{}.port.baudrate".format(self.key, self.__identifier))
        if exit_reader_port_baudrate is not None:
            exit_reader_port_baudrate.update_handlers = self.__exit_reader_cb

        exit_reader_port_name = self._registers.by_name("{}.exit_reader_{}.port.name".format(self.key, self.__identifier))
        if exit_reader_port_name is not None:
            exit_reader_port_name.update_handlers = self.__exit_reader_cb
            exit_reader_port_name.update()


        # Create exit button.
        exit_button_input = self._registers.by_name("{}.exit_button_{}.input".format(self.key, self.__identifier))
        if exit_button_input is not None:
            exit_button_input.update_handlers = self.__exit_btn_input_cb
            exit_button_input.update()

        # Create window closed sensor.
        window_closed_input = self._registers.by_name("{}.window_closed_{}.input".format(self.key, self.__identifier))
        if window_closed_input is not None:
            window_closed_input.update_handlers = self.__window_closed_input_cb
            window_closed_input.update()

        # Create door closed sensor.
        door_closed_input = self._registers.by_name("{}.door_closed_{}.input".format(self.key, self.__identifier))
        if door_closed_input is not None:
            door_closed_input.update_handlers = self.__door_closed_input_cb
            door_closed_input.update()

        # Create PIR sensor.
        pir_input = self._registers.by_name("{}.pir_{}.input".format(self.key, self.__identifier))
        if pir_input is not None:
            pir_input.update_handlers = self.__pir_input_cb
            pir_input.update()


        # Create locking mechanism.
        lock_mechanism_output = self._registers.by_name("{}.lock_mechanism_{}.output".format(self.key, self.__identifier))
        if lock_mechanism_output is not None:
            lock_mechanism_output.update_handlers = self.__lock_mechanism_output_cb
            lock_mechanism_output.update()

        # Door window blind.
        door_window_blind_output = self._registers.by_name("{}.door_window_blind_{}.output".format(self.key, self.__identifier))
        if door_window_blind_output is not None:
            door_window_blind_output.update_handlers = self.__door_window_blind_output_cb
            door_window_blind_output.update()

        # Door window blind.        
        self._registers.add_callback(
            "{}.door_window_blind_{}.value".format(self.key, self.__identifier),
            self.__door_window_blind_value_cb,
            update=True)

    def __set_zone_occupied(self, value):

        reg_occupation = self._registers.by_name("{}.zone_{}_occupied".format(self.key, self.__identifier))
        if reg_occupation is not None:
            if reg_occupation.value != value:
                reg_occupation.value = value

#endregion

#region Private Methods (Card Reader)

    def __check_card_state(self, card_id):

        # Request - Eml6287
        card_state = CardState.NONE

        allowed_len = len(self.__allowed_attendant)
        checked_index = 0
        for card in self.__allowed_attendant:
            if card["card_id"] == card_id:
                now = time.time()

                if now < card["valid_until"]:
                    card_state = CardState.Allowed
                    break

                else:
                    card_state = CardState.Expired
                    break
            
            checked_index += 1
            if checked_index == allowed_len and card_state == CardState.NONE:
                card_state = CardState.NotAllowed

        return card_state

    def __cb_read_card(self, card_id, serial_number):

        # Set flag to open the door.
        card_state = self.__check_card_state(card_id)
        if card_state == CardState.Allowed:
            if self.__open_door_flag == 0:
                self.__open_door_flag = 1

        if self.__on_card_cb is not None:
            self.__on_card_cb(card_id, serial_number, card_state.value)

    def __delete_reader(self, reader):

        if reader is not None:

            reader.shutdown()

            while reader.reader_state == CardReaderState.RUN:
                pass

            del reader

    def __update_entry_reader(self):
        """Update entry reader state."""

        if self.__entry_reader is not None:

            # Update card reader.
            self.__entry_reader.update()

            if self.__entry_reader.reader_state == CardReaderState.STOP:

                message = "Card reader {}; State {}; Port {}."\
                    .format(self.__entry_reader.serial_number, \
                            self.__entry_reader.reader_state, \
                            self.__entry_reader.port_name)

                GlobalErrorHandler.log_hardware_malfunction(self.__logger, message)

                self.__entry_reader.init()

            if self.__entry_reader.reader_state == CardReaderState.NONE:

                message = "Card reader {}; State {}."\
                    .format(self.__entry_reader.serial_number, self.__entry_reader.reader_state)

                GlobalErrorHandler.log_hardware_malfunction(self.__logger, message)

                self.__entry_reader.init()

    def __update_exit_reader(self):
        """Update exit reader state."""

        if self.__exit_reader is not None:

            # Update card reader.
            self.__exit_reader.update()

            if self.__exit_reader.reader_state == CardReaderState.STOP:

                message = "Card reader {}; State {}; Port {}."\
                    .format(self.__exit_reader.serial_number, \
                            self.__exit_reader.reader_state, \
                            self.__exit_reader.port_name)

                GlobalErrorHandler.log_hardware_malfunction(self.__logger, message)

                self.__exit_reader.init()

            if self.__exit_reader.reader_state == CardReaderState.NONE:

                message = "Card reader {}; State {}."\
                    .format(self.__exit_reader.serial_number, self.__entry_reader.reader_state)

                GlobalErrorHandler.log_hardware_malfunction(self.__logger, message)

                self.__exit_reader.init()

#endregion

#region (PLC)

    def __read_exit_button(self):

        state = False

        if self._controller.is_valid_gpio(self.__exit_btn_input):
            state = self._controller.digital_read(self.__exit_btn_input)

        return state

    def __read_window_tamper(self):

        state = False

        if self._controller.is_valid_gpio(self.__window_closed_input):
            state = self._controller.digital_read(self.__window_closed_input)

        return state

    def __read_door_tamper(self):

        state = False

        if self._controller.is_valid_gpio(self.__door_closed_input):
            state = self._controller.digital_read(self.__door_closed_input)

        return state

    def __read_pir_sensor(self):

        state = False

        if self._controller.is_valid_gpio(self.__pir_input):
            state = self._controller.digital_read(self.__pir_input)

        return state

    def __set_lock_mechanism(self, value=0):

        if self._controller.is_valid_gpio(self.__lock_mechanism_output):
            self._controller.digital_write(self.__lock_mechanism_output, value)

    def __set_door_window_blind(self, value=0):

        if self._controller.is_valid_gpio(self.__door_window_blind_output):
            self._controller.digital_write(self.__door_window_blind_output, value)

#endregion

#region Protected Methods

    def _init(self):
        """Initialize the plugin.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} {}".format(self.name, self.__identifier))

        # Setup open timer to 10 seconds.
        self.__open_timer = Timer(10)

        # Setup presence timer to 60 seconds.
        self.__presence_timer = Timer(60)

        self.__init_registers()

    def _update(self):
        """Update the plugin.
        """

        # Update inputs.
        btn_state = self.__read_exit_button()
        door_tamper_state = self.__read_door_tamper()
        pir_sensor_state = self.__read_pir_sensor()
        window_tamper_state = self.__read_window_tamper()

        self.__update_entry_reader()
        self.__update_exit_reader()

        # Check if the button is pressed.
        if btn_state:
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
        if door_tamper_state:
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

        # If one of the sensor are activated, set occupation flag to true.
        if door_tamper_state or pir_sensor_state or window_tamper_state:
            self.__presence_timer.update_last_time()
            self.__set_zone_occupied(True)

        # Else, run the expiration timer.
        else:
            self.__presence_timer.update()
            if self.__presence_timer.expired:
                self.__presence_timer.clear()
                self.__set_zone_occupied(False)

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {} {}".format(self.name, self.__identifier))
        self.__set_lock_mechanism(0)
        self.__set_door_window_blind(0)
        self.__delete_reader(self.__entry_reader)
        self.__delete_reader(self.__exit_reader)

#endregion

#region Public Methods

    def on_card(self, callback):
        """Set reader read calback."""

        if callback is None:
            return

        self.__on_card_cb = callback

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

        for key in ids:
            record = ids[key]
            self.add_allowed_attendant(record)

#endregion
