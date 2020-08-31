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

from threading import Thread

from http.server import HTTPServer

from services.http.request_handler import RequestHandler

from utils.logger import get_logger

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

class Server:
    """Local WEB server."""

#region Attributes

    __logger = None
    """Logger"""

    __host = "127.0.0.1"
    """Host"""

    __port = 8889
    """Port"""

    __server = None
    """WEB server."""

    __thread = None
    """Thread"""

#endregion

#region Constructor

    def __init__(self, host="127.0.0.1", port=8889):

        if host is not None:
            self.__host = host

        if port is not None:
            self.__port = port

        # Create logger.
        self.__logger = get_logger(__name__)

#endregion

#region Properties

    @property
    def is_alive(self):
        """Is alive flag."""

        state = False

        if self.__thread is not None:
            state = self.__thread.is_alive()

        return state

#endregion

#region Private Methods

    def __worker(self, args):
        self.__server.serve_forever()

#endregion

#region Public Methods

    def start(self):
        """Start the server."""

        # Create two threads as follows
        try:
            if self.__thread is None:

                # Create
                self.__thread = Thread(target=self.__worker, args=(33,))
                self.__server = HTTPServer((self.__host, self.__port), RequestHandler)

                # Start if not.
                if not self.__thread.is_alive():
                    self.__thread.start()

                    self.__logger.info("Start WEB service.")

        except Exception as exception:
            self.__logger.error(exception)

    def stop(self):
        """Stop the server."""

        try:
            if self.__thread is not None:

                # If it is alive join.
                if self.__thread.is_alive():

                    # Shutdown the server.
                    self.__server.shutdown()

                    # Wait to stop.
                    while self.__thread.is_alive():
                        pass

                    self.__thread.join()

                    # Delete
                    self.__thread = None
                    self.__server = None

                    self.__logger.info("Stop WEB service.")

        except Exception as exception:
            self.__logger.error(exception)

#endregion
