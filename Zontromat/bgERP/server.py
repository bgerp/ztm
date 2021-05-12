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

from flask import Flask, request, make_response

from utils.logger import get_logger

from services.http.server import Server as HTTPServer

from bgERP.session import Session

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
    """bgERP service communicator"""

#region Attributes

    __logger = None
    """Logger
    """

    __sync_cb = None
    """bgERP update callback handler.
    """

    __get_registers = None
    """Get register callback.
    """

    __set_registers = None
    """Set register callback.
    """

    __session = None
    """Session control."""

#endregion

#region Constructor

    def __init__(self, **config):
        """Constructor
        """

        port = 8890
        if "port" in config:
            port = config["port"]

        super().__init__(target=self, name=__name__, port=port)

        self.__logger = get_logger(__name__)

        self.__session = Session()
        self.__session.load()

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

        @self._app.route("/api/v1/bgerp/sync", methods=["POST"])
        def sync_post():
            """bgERP registers update callback."""
            # TODO: Add authentication when requesting information.

            if self.__sync_cb is not None:
                self.__sync_cb()

            response = make_response()
            response.headers["Content-Type"] = "application/json; charset=utf-8"

            return response

        @self._app.route("/api/v1/bgerp/registers/get", methods=["POST"])
        def get_register_post():
            """Callback that set the register.
            """
            # TODO: Add authentication when requesting information.
            # (Request to have WEB API for work with registers. MG @ 15.01.2021)

            json_data = {}
            response = "{}", 200
            token = ""
                        
            if request.data is not None and request.data != "":
                json_data = json.loads(request.data)

            if "token" in json_data:
                token = json_data["token"]

            if token is None or "":
                return "Invalid token.", 401

            if token != self.__session.session:
                return "Invalid token.", 401

            if self.__get_registers is not None:
                registers = self.__get_registers(json_data)

            response = make_response(registers)
            response.headers["Content-Type"] = "application/json; charset=utf-8"

            return response

        @self._app.route("/api/v1/bgerp/registers/set", methods=["POST"])
        def set_register_post():
            """Callback that get the register.
            """
            # TODO: Add authentication when requesting information.
            # (Request to have WEB API for work with registers. MG @ 15.01.2021)

            json_data = {}
            response = "{}", 200
            token = ""
                        
            if request.data is not None and request.data != "":
                json_data = json.loads(request.data)

            if "token" in json_data:
                token = json_data["token"]

            if token is None or "":
                return "Invalid token.", 401

            if token != self.__session.session:
                return "Invalid token.", 401

            if self.__set_registers is not None:
                registers = self.__set_registers(json_data)

            response = make_response(registers)
            response.headers["Content-Type"] = "application/json; charset=utf-8"

            return response

#endregion

#region Public Methods

    def set_sync_cb(self, callback):
        """Set bgERP update callback"""

        self.__sync_cb = callback

    def set_registers_cb(self, **config):
        """Set callbacks for the handlers.
        """
        # (Request to have WEB API for work with registers. MG @ 15.01.2021)

        if "get_cb" in config:
            self.__get_registers = config["get_cb"]

        if "set_cb" in config:
            self.__set_registers = config["set_cb"]

#endregion
