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

import argparse
import time
import sys

from neuron import Neuron
from utils.utils import time_measure

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

__neuron = None

@time_measure
def test_function():
    """Test function"""

    global __neuron

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="176.33.1.72", help="IP Address")
    parser.add_argument("--port", type=int, default=8080, help="Port")
    parser.add_argument("--dev", type=str, default="temp", help="Device")
    parser.add_argument("--circuit", type=str, default="28FFC4EE00170349", help="Circuit")

    args = parser.parse_args()

    __neuron = Neuron(args.ip, args.port)
    __neuron.update()
    device = __neuron.get_device(args.dev, args.circuit)

    print(device)

def main():
    """Main"""

    print('1W get device test; Time: %.3f' % round(test_function, 3))

def kb_interupt():
    """Keyboard interupt handler."""

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        kb_interupt()
