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

import traceback
from threading import Thread

from flask import Flask, request
from werkzeug.serving import make_server

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

class Server(Thread):
    """Base HTTP threaded server."""

#region Attributes

    _app = None
    """Flask App."""

    __port = 10203
    """Port"""

    __host = "0.0.0.0"
    """Host"""

#endregion

#region Properties

    @property
    def app(self):
        """App instance."""

        return self._app

#endregion

#region Constructor

    def __init__(self, **kwargs):
        """Constructor"""

        super().__init__(target=kwargs["target"])
        self.setDaemon(True)

        if "port" in kwargs:
            self.__port = kwargs["port"]

        if "host" in kwargs:
            self.__host = kwargs["host"]

        self._app = Flask(kwargs["name"])

#endregion

#region Private Methods

    def __shutdown_server(self):

        func = request.environ.get('werkzeug.server.shutdown')

        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        func()

#endregion

#region Public Methods

    def run(self):
        """Run the server."""

        self._app.run(host=self.__host, port=self.__port,\
                    debug=True, use_reloader=False)

    def stop(self):
        """Stop the server."""

        try:
            # If it is alive join.
            if self.is_alive():

                self.__shutdown_server()
                self.join()

        except Exception as exception:
            print(exception)

#endregion
