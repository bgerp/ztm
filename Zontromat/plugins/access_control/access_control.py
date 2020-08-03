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

from utils.logger import get_logger
from utils.timer import Timer

from plugins.base_plugin import BasePlugin
from plugins.access_control.security_zone import SecurityZone

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


class AccessControl(BasePlugin):
    """Access control and security."""

#region Attributes

    __logger = None
    """Logger"""

    __last_minute_attendees = []
    """Last 30 attendees"""

    __is_empty_timer = None
    """Is empty timer."""

    __security_zone_1 = None
    """Security zone 1"""

    __security_zone_2 = None
    """Security zone 2"""

#endregion

#region Destructor

    def __del__(self):
        """Destructor"""

        del self.__logger
        del self.__security_zone_1
        del self.__security_zone_2

#endregion

#region Private Methods

    def __allowed_attendees_cb(self, register):

        # Check data type.
        if not register.is_json():
            self._log_bad_value_register(self.__logger, register)
            return

        self.__security_zone_1.add_allowed_attendees(register.value)
        self.__security_zone_2.add_allowed_attendees(register.value)

    def __is_empty_timeout_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            self._log_bad_value_register(self.__logger, register)
            return

        if self.__is_empty_timer.expiration_time != register.value:
            self.__is_empty_timer.expiration_time = register.value

    def __set_zone_occupied(self, flag):

        is_empty = self._registers.by_name(self._key + ".zone_occupied")
        if is_empty is not None:
            is_empty.value = flag

        is_empty = self._registers.by_name("env.is_empty")
        if is_empty is not None:
            is_empty.value = flag

    def __update_occupation(self):

        pir_1_value = False
        pir_1 = self._registers.by_name(self._key + ".pir.state")
        if pir_1 is not None:
            pir_1_value = pir_1.value

        pir_2_value = False
        pir_2 = self._registers.by_name(self._key + ".pir2.state")
        if pir_2 is not None:
            pir_2_value = pir_2.value

        dc_1_value = False
        cd_1 = self._registers.by_name(self._key + ".door_closed.state")
        if cd_1 is not None:
            dc_1_value = cd_1.value

        dc_2_value = False
        cd_2 = self._registers.by_name(self._key + ".door_closed2.state")
        if cd_2 is not None:
            dc_2_value = cd_2.value

        wc_1_value = False
        wc_1 = self._registers.by_name(self._key + ".window_closed.state")
        if wc_1 is not None:
            wc_1_value = wc_1.value

        wc_2_value = False
        wc_2 = self._registers.by_name(self._key + ".window_closed2.state")
        if wc_2 is not None:
            wc_2_value = wc_2.value

        # Apply OR for all the signals.
        occupation_state = \
            (pir_1_value or pir_2_value or dc_1_value or dc_2_value or wc_1_value or wc_2_value)

        # Clear time interval.
        if occupation_state:
            # Reset timer every time activity has present.
            self.__is_empty_timer.update_last_time()
            self.__set_zone_occupied(1)

        # Update is empty timer.
        self.__is_empty_timer.update()
        if self.__is_empty_timer.expired:
            self.__is_empty_timer.clear()

            # If no activity has present for 3600 second,
            # then the timer will expire and flag will be set to 0.
            self.__set_zone_occupied(0)

    def __filter_atendee_by_time(self, time_sec):

        # Create filter list.
        filtered_atendee = []
        
        # Reset delete flag.
        delete_flag = False

        # Now!
        time_now = time.time()

        # Filter all records.
        for attendee in self.__last_minute_attendees:

            # Calculate delta time.
            delta_t = time_now - attendee["ts"]

            # Filter
            if delta_t < time_sec:
                filtered_atendee.append(attendee)

            # Else mark for deletion.
            else:
                delete_flag = True

        # Execute the flag.
        if delete_flag:
            self.__last_minute_attendees.clear()
            self.__last_minute_attendees = filtered_atendee

    def __reader_read(self, card_id, reader_id):

        # Create a record.
        record = { \
            "ts": time.time(), \
            "card_id": card_id, \
            "reader_id": reader_id, \
        }

        # Append new record.
        self.__last_minute_attendees.append(record)

        self.__filter_atendee_by_time(60)

        # print(self.__last_minute_attendees)

        # Update last 60 seconds attendee list.
        last_minute_attendees = self._registers.by_name(self._key + ".last_minute_attendees")
        if last_minute_attendees is not None:
            str_data = str(self.__last_minute_attendees)
            last_minute_attendees.value = str_data


#endregion

#region Public Methods

    def init(self):

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

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

        # Security zone 1.
        self.__security_zone_1 = SecurityZone(self._registers, self._controller, 1)
        self.__security_zone_1.set_reader_read(self.__reader_read)
        self.__security_zone_1.init()

        # Security zone 2.
        self.__security_zone_2 = SecurityZone(self._registers, self._controller, 2)
        self.__security_zone_2.set_reader_read(self.__reader_read)
        self.__security_zone_2.init()

    def update(self):
        """Update"""

        self.__security_zone_1.update()
        self.__security_zone_2.update()
        self.__update_occupation()

    def shutdown(self):
        """Shutting down the reader."""

        self.__security_zone_1.shutdown()
        self.__security_zone_2.shutdown()
        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
