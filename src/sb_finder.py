#  sb_finder -- detect suspicious traffic in pcap files
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
import argparse
import sys
from scapy.all import sniff


def handle_options(args):
    """Handle commandline options.
    """
    parser = argparse.ArgumentParser(
       description="Find patterns in pcap files.")
    parser.add_argument(
        '-f', '--file', metavar='FILE', default=None, required=True,
        help="Input PCAP file to read from. `-' will read from stdin.",
        )
    args = parser.parse_args(args)
    return args


class Filter(object):
    def __init__(self, flt_expr, optimize=False, netmask=1):
        self.flt_expr = flt_expr
        self.optimize = optimize
        self.netmask = netmask


class Detector(Filter):
    """A detector is a list of packet filters.

    It is meant to represent some anomaly or event in a network stream, which
    can be detected by the filters applied.
    """
    def __init__(self, filters=(), severity=0, tags=[], message=None):
        self.filters = filters
        self.severity = severity
        self.tags = tags
        self.message = message

    def matching_filters(self, path):
        """Return the filters matching data in `path`.
        """
        result = []
        for flt in self.filters:
            pkts = sniff(offline=path, filter=flt.flt_expr)
            if len(pkts):
                result.append(flt)
        return result


def matches_filter(pkt, filt):
    if len(sniff(offline=pkt, filter=filt)):
        return True
    return False


def main(args=None):
    """Main programme.
    """
    if args is None:
        args = sys.args[1:]
    options = handle_options(args)

