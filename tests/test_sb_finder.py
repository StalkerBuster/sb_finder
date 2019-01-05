import os
import pcapy
from sb_finder import matches_filter


def test_matches_filter():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    src = pcapy.open_offline(os.path.join(path, 'single_ip.pcap'))
    header, data = src.next()
    bpf = pcapy.compile(pcapy.DLT_EN10MB, 1350, "tcp", 0, 1)
    assert matches_filter(data, bpf) is True
