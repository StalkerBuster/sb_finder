#  sampler -- create samples in pcapng format
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
from scapy.all import sniff, wrpcap


class SampleMaker(object):
    """Create samples for stalkerbuster.
    """
    def __init__(self, dev=None, outpath='sample.pcapng'):
        self.dev = dev
        self.outpath = outpath
        self.sampling = False

    def update_outfile(self, pkts):
        """Append `pkts` into pcap file,
        """
        wrpcap(self.outpath, pkts, append=True)

    def start(self):
        assert not self.sampling  # only one recording at a time
        self.sampling = True
        sniff(iface=self.dev, prn=self.update_outfile)

    def stop(self):
        pass
