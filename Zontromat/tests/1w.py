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
import sys

from controllers.controller_factory import ControllerFactory
from utils.performance_profiler import PerformanceProfiler
from controllers.update_state import UpdateState

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

__controller = None

__performance_profiler = PerformanceProfiler()

def __on_change(current, peak, passed_time):

    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    print(f"Total time: {passed_time:.3f} sec")

@__performance_profiler.profile
def main():
    """Main"""

    global __controller, __performance_profiler

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="http://127.0.0.1", help="IP Address")
    parser.add_argument("--port", type=int, default=80, help="Port")
    parser.add_argument("--dev", type=str, default="temp", help="Device")
    parser.add_argument("--circuit", type=str, default="28FFC4EE00170349", help="Circuit")

    args = parser.parse_args()

    __performance_profiler.enable_mem_profile = True
    __performance_profiler.enable_time_profile = True
    __performance_profiler.max_mem = 0.03
    __performance_profiler.on_change(__on_change)

    host = "{}:{}/".format(args.host, args.port)

    # Create Neuron.
    __controller = ControllerFactory.create(\
        vendor="unipi",\
        model="M503",\
        serial=25,\
        host=host,\
        timeout=5)

    state = __controller.update()

    if state == UpdateState.Failure:
        print("Unable to connect the controller.")

    elif state == UpdateState.Success:
        device = __controller.get_device(args.dev, args.circuit)
        print(device)

def kb_interupt():
    """Keyboard interupt handler."""

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        kb_interupt()

    except Exception as e:
        print(e)
