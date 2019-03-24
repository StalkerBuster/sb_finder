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
import wifi
from wifi import Cell


def get_avail_netdevs():
    """Get a list of all network devices.

    We run `ifconfig` and parse the output.
    """
    lines = subprocess.check_output("ifconfig").decode("utf-8")
    devnames = re.findall("^([a-zA-Z0-9_]+)", lines, re.M)
    return devnames


def get_avail_wlans():
    """Get available wireless networks (SSIDs)
    """
    nets = []
    for devname in get_avail_netdevs():
        try:
            nets.extend(Cell.all(devname))
        except wifi.exceptions.InterfaceError:
            pass
    return list(set([x.ssid for x in nets]))


def get_current_wlan():
    """Get the current SSID

    as a string or `None` if no connection is active.
    """
    try:
        lines = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8")
    except subprocess.CalledProcessError:
        # status 255 can mean: no active connection
        return None
    return lines.split('\n')[0]


def select_wlan(ssid, password, iface=None):
    cell = list(wifi.Cell.all(iface))[0]
    scheme = wifi.Scheme.for_cell(iface, ssid, cell, password)
    scheme.activate()


def unselect_wlan():
    pass


class NetworkManager(object):

    get_current_wlan = staticmethod(get_current_wlan)

    @classmethod
    def get_connections(cls):
        """Get UUIDs of all locally defined NM connections
        """
        lines = subprocess.check_output(
                ["nmcli", "--fields", "type,uuid", "con", "show"]
                ).decode("utf-8")
        tuples = [line.split() for line in lines.split("\n")]
        return set([x[1] for x in tuples if "wifi" in x])

    @classmethod
    def get_avail_wlans(cls):
        lines = subprocess.check_output(
                ["nmcli", "-t", "dev", "wifi"]).decode("utf-8")
        ssids = re.findall("^ :([^:]*):.+", lines, re.M)
        return ssids

    @classmethod
    def select_wlan(ssid, password, iface=None):
        lines = subprocess.check_output(
                ["nmcli", "con", "up", ssid]).decode("utf-8")
