
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
from http.server import BaseHTTPRequestHandler
from urllib import parse

from services.http.register_handler import RegisterHandler

class RequestHandler(BaseHTTPRequestHandler):
    """Request Handler"""

#region Attributes

    __api_path_evok = "/api/evok-webhooks"
    """API path to EVOK handler."""

#endregion

#region Private Methods

    def __api_evok_webhooks_handler(self):

        # Get content length.
        content_length = self.headers["Content-Length"]
        content_length = int(content_length)

        # Get body request.
        req_body = self.rfile.read(content_length)
        req_body = req_body.decode("utf-8")

        # Convert to JSON object.
        req_body = json.loads(req_body)

        # Update handler.
        RegisterHandler.update(req_body)

        # The response.
        self.send_response(200)
        self.send_header("Content-Type",
                         "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))

#endregion

#region Public Methods

    def do_POST(self):
        """Execute when POST request comes in."""

        parsed_path = parse.urlparse(self.path)

        if parsed_path.path == self.__api_path_evok:
            self.__api_evok_webhooks_handler()

        else:
            # The response.
            self.send_response(200)
            self.send_header("Content-Type",
                             "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("OK".encode("utf-8"))

    def do_GET(self):
        """Execute when GET request comes in."""

        parsed_path = parse.urlparse(self.path)

        if parsed_path.path == self.__api_path_evok:
            self.__api_evok_webhooks_handler()

        else:
            # The response.
            self.send_response(200)
            self.send_header("Content-Type",
                             "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("OK".encode("utf-8"))

#endregion
