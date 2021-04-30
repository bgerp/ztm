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

from devices.HangzhouAirflowElectricApplications.f3p146ec072600.f3p146ec072600 import F3P146EC072600 as Fan

from controllers.controller_factory import ControllerFactory as CF

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

def main():
    """Main function.
    """

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--port", type=str, default="COM10", help="Serial port.")
    parser.add_argument("--unit", type=int, default=1, help="Unit ID.")
    parser.add_argument("--plc_vendor", type=str, default="dummy", help="Controller vendor.")
    parser.add_argument("--plc_model", type=str, default="dummy", help="Controller model.")

    # Take arguments.
    args = parser.parse_args()

    # Get args.
    unit = args.unit
    port = args.port
    plc_vendor = args.plc_vendor
    plc_model = args.plc_model

    # PLC configuration.
    plc_config = {
            "vendor": plc_vendor,
            "model": plc_model
        }
    controller = CF.create(plc_config)

    # Convector interface.
    convector_config = {
            "name": "Test Fan",
            "output": "A0",
            "controller": controller
        }
    fan = Fan(convector_config)
    fan.init()

    #---------------------------------------------------------------------------#
    # Test case
    #---------------------------------------------------------------------------#
    set_point = 100
    fan.min_speed = set_point
    state = fan.min_speed
    is_ok = set_point == state
    print("Setpoint: {}; State: {}; IS OK: {}".format(set_point, state, is_ok))
    assert is_ok, "Incorrect state."

    #---------------------------------------------------------------------------#
    # Test case
    #---------------------------------------------------------------------------#
    set_point = 0
    fan.min_speed = set_point
    state = fan.min_speed
    is_ok = set_point == state
    print("Setpoint: {}; State: {}; IS OK: {}".format(set_point, state, is_ok))
    assert is_ok, "Incorrect state."

    #---------------------------------------------------------------------------#
    # Test case
    #---------------------------------------------------------------------------#
    set_point = 0
    fan.max_speed = set_point
    state = fan.max_speed
    is_ok = set_point == state
    print("Setpoint: {}; State: {}; IS OK: {}".format(set_point, state, is_ok))
    assert is_ok, "Incorrect state."

    #---------------------------------------------------------------------------#
    # Test case
    #---------------------------------------------------------------------------#
    set_point = 100
    fan.max_speed = set_point
    state = fan.max_speed
    is_ok = set_point == state
    print("Setpoint: {}; State: {}; IS OK: {}".format(set_point, state, is_ok))
    assert is_ok, "Incorrect state."
    
    #---------------------------------------------------------------------------#
    # Test case
    #---------------------------------------------------------------------------#
    set_point = 0
    fan.set_state(set_point)
    state = fan.get_state()
    is_ok = set_point == state
    print("Setpoint: {}; State: {}; IS OK: {}".format(set_point, state, is_ok))
    if is_ok:
        time.sleep(5)
    assert is_ok, "Incorrect state."

if __name__ == "__main__":
    main()

# TODO: ALL controllers should have abilities to read and write all their resources.
