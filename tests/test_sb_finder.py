import os
import pcapy
from sb_finder import matches_filter


def test_matches_filter_detects_ip_packets():
    # we can detect certain simple packets.
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    src = pcapy.open_offline(os.path.join(path, 'single_ip.pcap'))
    header, data = src.next()
    bpf_ip = pcapy.compile(src.datalink(), 1350, "ip", 0, 1)
    bpf_tcp = pcapy.compile(src.datalink(), 1350, "tcp", 0, 1)
    assert matches_filter(data, bpf_ip) is True
    assert matches_filter(data, bpf_tcp) is False


def test_matches_filter_detects_dst():
    # we can filter by destination ip
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    src = pcapy.open_offline(os.path.join(path, 'single_ip.pcap'))
    header, data = src.next()
    bpf = pcapy.compile(src.datalink(), 1350, "dst 4.3.2.1", 0, 1)
    assert matches_filter(data, bpf) is True
