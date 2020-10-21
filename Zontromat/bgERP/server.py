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

import json

from flask import Flask, request

from utils.logger import get_logger

from services.http.server import Server as HTTPServer

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

class Server(HTTPServer):
    """bgERP service communicator"""

#region Attributes

    __logger = None
    """Logger"""

    __evok_update_cb = None
    """EVOK Update callback handler."""

    __bgerp_update_cb = None
    """bgERP update callback handler."""

#endregion

#region Constructor

    def __init__(self, name):
        super().__init__(target=self, name=name)

        self.__logger = get_logger(__name__)

        self.__set_routs()

#endregion

#region Private Methods

    def __set_routs(self):
        """Set API routs."""

        @self._app.errorhandler(Exception)
        def error_handler(error):
            """Error handler.

            Args:
                error (mixed): Error

            Returns:
                list: Response
            """

            self.__logger.error(error)

            return "Unknown Error", 500

        @self._app.route("/bgerp/sync", methods=["POST"])
        def bgerp_api_post():
            """bgERP registers update callback."""
            # TODO: Add authentication when requesting information.

            if self.__bgerp_update_cb is not None:
                self.__bgerp_update_cb("OK")

            return ""

        # Evok event handler.
        @self._app.route("/api/evok-webhooks", methods=["POST"])
        def evok_api_post():
            """Evok WEB hooks for POST method."""

            data = request.get_data(as_text=True)
            if data is not None:
                json_data = json.loads(data)
                if json_data is not None:
                    for item in json_data:
                        if self.__evok_update_cb is not None:
                            self.__evok_update_cb(item)

            return ""

#endregion

#region Public Methods

    def set_evok_cb(self, callback):
        """Set update callback."""

        self.__evok_update_cb = callback

    def set_bgerp_cb(self, callback):
        """Set bgERP update callback"""

        self.__bgerp_update_cb = callback

#endregion
