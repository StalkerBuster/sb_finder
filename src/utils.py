#  utils - helpful stuff for setting up networks and the like
#  Copyright (C) 2019  StalkerBuster
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
import re
import subprocess
from wifi import Cell, Scheme


def get_avail_netdevs():
    """Get a list of all net devices.

    We run `ifconfig` and parse the output.
    """
    lines = subprocess.check_output("ifconfig").decode("utf-8")
    devnames = re.findall("^([a-zA-Z0-9_]+)", lines, re.M)
    return devnames


def get_avail_wlans():
    """Get available wireless networks (SSIDs)
    """
    nets = Cell.all()
    return [x for x in nets]


def get_current_clan():
    pass


def select_wlan(ssid, password):
    pass


def unselect_wlan():
    pass
