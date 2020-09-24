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

import signal
import nfc
import ndef
from threading import Thread

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

#region Variables

__clf = None
"""Contactless front-end."""

__time_to_stop = False
"""Time to stop flag."""

#endregion

def beam(llc):
    global __time_to_stop, __clf

    __time_to_stop = True

    print(llc)

    # snep_client = nfc.snep.SnepClient(llc)
    # snep_client.put_records([ndef.TextRecord("Traby")])

    # return

    ndef_obj = llc.ndef
    if ndef_obj is not None:
        print(ndef_obj)
        records = ndef_obj.records
        if records is not None:
            for record in records:
                if record.type == "text/vcard":
                    content = record.data.decode("utf-8")
                    print(content)

        # snep_client.put_records([ndef.UriRecord("http://nfcpy.org")])

def on_startup(target):

    print(target)

    return target

def connected(llc):

    state = False

    try:
        Thread(target=beam, args=(llc,)).start()
        state = True
    except:
        pass

    return state

def interupt_handler(signum, frame):
    """Interupt handler."""

    global __time_to_stop, __clf

    __time_to_stop = True

    if signum == 2:
        print("Stopped by interupt.")

    elif signum == 15:
        print("Stopped by termination.")

    else:
        print("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    __clf.close()

def main():
    """Main"""

    global __time_to_stop, __clf

    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    __clf = nfc.ContactlessFrontend("usb:072f:2200")
    # clf = nfc.ContactlessFrontend("usb")
    # clf = nfc.ContactlessFrontend("udp")
    state = __clf.connect(rdwr={'on-startup': on_startup, "on-connect": connected})
    # state = __clf.connect(llcp={'on-startup': on_startup, "on-connect": connected})


    # for record in tag.ndef.records:
    #     print(record)

    if not state:
        __time_to_stop = True

    while not __time_to_stop:
        pass

    __clf.close()


if __name__ == "__main__":
    main()
