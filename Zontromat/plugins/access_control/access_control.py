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
import json

from utils.logger import get_logger
from utils.timer import Timer

from plugins.base_plugin import BasePlugin
from plugins.access_control.security_zone import SecurityZone

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


class AccessControl(BasePlugin):
    """Access control and security."""

#region Attributes

    __logger = None
    """Logger"""

    __last_minute_attendees = []
    """Last minute attendees"""

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
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__security_zone_1.add_allowed_attendees(register.value)
        self.__security_zone_2.add_allowed_attendees(register.value)

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
            obj = json.loads(last_minute_attendees.value)
            obj.append(self.__last_minute_attendees)
            last_minute_attendees.value = json.dumps(obj[0])

#endregion

#region Public Methods

    def init(self):

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Card reader allowed IDs.
        allowed_attendees = self._registers.by_name(self._key + ".allowed_attendees")
        if allowed_attendees is not None:
            allowed_attendees.update_handlers = self.__allowed_attendees_cb

        # Security zone 1.
        self.__security_zone_1 = SecurityZone(\
            registers=self._registers, controller=self._controller,\
            identifier=1, key=self._key, name="Security Zone")

        self.__security_zone_1.set_reader_read(self.__reader_read)
        self.__security_zone_1.init()

        # Security zone 2.
        self.__security_zone_2 = SecurityZone(\
            registers=self._registers, controller=self._controller,\
            identifier=2, key=self._key, name="Security Zone")
        
        self.__security_zone_2.set_reader_read(self.__reader_read)
        self.__security_zone_2.init()

    def update(self):
        """Update"""

        self.__security_zone_1.update()
        self.__security_zone_2.update()

    def shutdown(self):
        """Shutting down the reader."""

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__security_zone_1.shutdown()
        self.__security_zone_2.shutdown()

#endregion
