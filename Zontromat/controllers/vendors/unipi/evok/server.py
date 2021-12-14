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

class Server(HTTPServer):
    """EVOK webhook server."""

#region Attributes

    __logger = None
    """Logger"""

    __webhook_cb = None
    """EVOK callback handler."""

#endregion

#region Constructor

    def __init__(self, **config):
        """Constructor
        """

        port = 8889
        if "port" in config:
            port = config.get("port", 8889)

        super().__init__(target=self, name=__name__, port=port)

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

        @self._app.route("/api/v1/evok/webhooks", methods=["POST"])
        def evok_webhook_post():
            """EVOK webhook."""

            json_data = None
            registers = None

            if "registers" in request.form:
                registers = request.form["registers"]
                registers = registers.replace("\\", "")
                registers = registers[1:-1]

            if registers is not None:
                json_data = json.loads(registers)

            if self.__webhook_cb is not None:
                self.__webhook_cb(json_data)

            return ""

#endregion

#region Public Methods

    def set_cb(self, callback):
        """Set bgERP update callback"""

        self.__webhook_cb = callback

#endregion
