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
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin
from plugins.ac.security_zone import SecurityZone

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

__class_name__ = "AccessControl"
"""Plugin class name."""

#endregion


class AccessControl(BasePlugin):
    """Access control and security."""

#region Attributes

    __logger = None
    """Logger"""

    __last_update_cycle_attendees = []
    """Last update cycle attendees"""

    __zones = {}
    """Security zones."""

#endregion

#region Destructor

    def __del__(self):
        """Destructor"""

        for zone in self.__zones:
            if zone is not None:
                del zone

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (Registers)

    def __allowed_attendees_cb(self, register):

        # Check data type.
        if not ((register.data_type == "json") or (register.data_type == "str")):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # If the register is str convert it to JSON. (This is fix.)
        content = []
        if register.data_type == "str":
            content = json.loads(register.value)
        else:
            content = register.value

        # Add allowed attendees.
        for key in self.__zones:
            self.__zones[key].add_allowed_attendees(content)

    def __get_occupation_flags(self):

        zones_count = 0
        reg_zones_count = self._registers.by_name("ac.zones_count")
        if reg_zones_count is not None:
            zones_count = reg_zones_count.value

        zones_occupation_flags = []
        for index in range(zones_count):

            # To human readable registers index.
            index += 1

            # Sinthesize the name of the occupation flag.
            register_name = "ac.zone_{}_occupied".format(index)

            # If there is no one at the zone, just turn off the lights.
            ac_zone_occupied = self._registers.by_name(register_name)
            if ac_zone_occupied is not None:
                zones_occupation_flags.append(ac_zone_occupied.value)

        return zones_occupation_flags

    def __set_envm_is_empty(self, flag):

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            is_empty.value = flag

#endregion

#region Private Methods

    def __filter_atendee_by_time(self, time_sec):

        # Create filter list.
        filtered_atendees = self.__last_update_cycle_attendees.copy()
        filtered_atendees.clear()

        # Reset delete flag.
        delete_flag = False

        # Now!
        time_now = time.time()

        # Filter all records.
        for attendee in self.__last_update_cycle_attendees:

            # Calculate delta time.
            delta_t = time_now - attendee["ts"]

            # Filter
            if delta_t < time_sec:
                filtered_atendees.append(attendee)

            # Else mark for deletion.
            else:
                delete_flag = True

        # Execute the flag.
        if delete_flag:
            self.__last_update_cycle_attendees.clear()
            for atendee in filtered_atendees:
                self.__last_update_cycle_attendees.append(atendee)

    def __on_card_cb(self, card_id, reader_id, card_state):

        # Create a record.
        record = { \
            "ts": time.time(), \
            "card_id": card_id, \
            "reader_id": reader_id, \
            # Request - Eml6287
            "card_state": card_state, \
        }

        # Append new record.
        self.__last_update_cycle_attendees.append(record)

        self.__filter_atendee_by_time(60)

        # print(self.__last_update_cycle_attendees)

        # Update last 60 seconds attendee list.
        last_minute_attendees = self._registers.by_name(self.key + ".last_update_attendees")
        if last_minute_attendees is not None:
            
            if last_minute_attendees.data_type == "str":

                obj = json.loads(last_minute_attendees.value)

                for attendee in self.__last_update_cycle_attendees:
                    obj.append(attendee)

                last_minute_attendees.value = json.dumps(obj)

#endregion

#region Public Methods

    def _init(self):
        """Init the plugin.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Card reader allowed IDs.
        zones_count = 0
        reg_zones_count = self._registers.by_name(self.key + ".zones_count")
        if reg_zones_count is not None:
            zones_count = reg_zones_count.value

        # Name the zones.
        prototype = "AC_{}"
        zones_count += 1
        for index in range(1, zones_count):

            # Create name.
            name = prototype.format(index)

            # Register the zone.
            self.__zones[name] = SecurityZone(\
                registers=self._registers, controller=self._controller,\
                identifier=index, key=self.key, name="Security Zone")

            # Add on card callback. 
            self.__zones[name].on_card(self.__on_card_cb)

            # Initialize the module.
            self.__zones[name].init()


        # Card reader allowed IDs.
        allowed_attendees = self._registers.by_name(self.key + ".allowed_attendees")
        if allowed_attendees is not None:
            allowed_attendees.update_handlers = self.__allowed_attendees_cb
            allowed_attendees.update()

    def _update(self):
        """Update the plugin.
        """

        for key in self.__zones:
            self.__zones[key].update()

        # Update occupation flags.
        occupation_flags = self.__get_occupation_flags()
        is_occupied = False
        for flag in occupation_flags:
            is_occupied = flag or is_occupied

        is_empty = not is_occupied

        self.__set_envm_is_empty(is_empty)

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        for key in self.__zones:
            self.__zones[key].shutdown()

#endregion
