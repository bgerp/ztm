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

from data.register import Register

from services.global_error_handler.error_codes import ErrorCodes

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

class GlobalErrorHandler:
    """Global error handler."""

#region Attributes

    __last_minute_errors = []
    """Circular queue for the last 100 errors."""

    __register = None
    """Register holding error messages."""

#endregion

#region Private Static Methods

    @staticmethod
    def __filter_error_by_time(time_sec):

        # Create filter list.
        filtered_atendee = []

        # Reset delete flag.
        delete_flag = False

        # Now!
        time_now = time.time()

        # Filter all records.
        for attendee in GlobalErrorHandler.__last_minute_errors:

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
            GlobalErrorHandler.__last_minute_errors.clear()
            GlobalErrorHandler.__last_minute_errors = filtered_atendee

#endregion

#region Public Static Methods

    @staticmethod
    def log_no_connection_erp(logger):
        """Log no connection with ERP."""

        message = "Communication lost with ERP."

        logger.error(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.NoConnectionWithERP)

    @staticmethod
    def log_no_connection_plc(logger):
        """Log bad value register"""

        message = "Communication lost with PLC."

        logger.error(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.NoConnectionWithPLC)

    @staticmethod
    def log_bad_register_value(logger, register):
        """Log bad value register"""

        message = "Inconsistent data for register {} with content {}"\
            .format(register.name, register.value)

        logger.error(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.BadRegisterValue)

    @staticmethod
    def log_bad_register_data_type(logger, register):
        """Log bad value register"""

        message = "Inconsistent data type for register {} with content {}"\
            .format(register.name, register.value)

        logger.error(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.BadRegisterDataType)

    @staticmethod
    def log_unexpected_register(logger, register):
        """Unexpected register."""

        message = "Add unexpected register {}; value: {}"\
            .format(register.name, register.value)

        logger.error(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.UnexpectedRegister)

    @staticmethod
    def log_register_not_found(logger, name):
        """Unexpected register."""

        message = "Register not found {}"\
            .format(name)

        logger.error(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.RegisterNotFound)

    @staticmethod
    def log_cart_reader_stop(logger, message):
        """Log card reader stop."""

        logger.warning(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.CartReaderStop)

    @staticmethod
    def log_cart_reader_none(logger, message):
        """Log cart reader none."""

        logger.warning(message)

        # Put error to the queue.
        GlobalErrorHandler.append(message, ErrorCodes.CartReaderNone)

    @staticmethod
    def append(message, err_code):
        """Put message to the queue."""

        error = \
            {
                "ts": time.time(),
                "err_code": err_code.value,
                "message": message
            }

        # Put to the end of the queue.
        GlobalErrorHandler.__last_minute_errors.append(error)

        GlobalErrorHandler.__filter_error_by_time(60)

        # Update the register.
        if GlobalErrorHandler.__register is not None:
            GlobalErrorHandler.__register.value = GlobalErrorHandler.__last_minute_errors

    @staticmethod
    def get_queue():
        """Get the whole queue."""

        return GlobalErrorHandler.__last_minute_errors

    @staticmethod
    def set_register(register):
        """Set register to be stored data."""

        if register is None:
            return

        if isinstance(register, Register):
            GlobalErrorHandler.__register = register

#endregion
