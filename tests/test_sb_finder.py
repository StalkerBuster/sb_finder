import os
from scapy.all import sniff
from sb_finder import matches_filter, Filter, Detector

SAMPLES_PATH = os.path.abspath(os.path.dirname(__file__))


def test_matches_filter_detects_ip_packets():
    # we can detect certain simple packets.
    path = os.path.join(SAMPLES_PATH, 'single_ip.pcap')
    data = sniff(offline=path)[-1]
    assert matches_filter(data, "ip") is True
    assert matches_filter(data, "tcp") is False


def notest_matches_filter_detects_dst():
    # we can filter by destination ip
    path = os.path.join(SAMPLES_PATH, 'single_ip.pcap')
    data = sniff(offline=path)[-1]
    assert matches_filter(data, "dst 4.3.2.1") is True
    assert matches_filter(data, "dst 1.2.3.4") is False


def test_filter_constructor():
    # we can construct filters
    f = Filter("dst 4.3.2.1")
    assert f.flt_expr == "dst 4.3.2.1"
    assert f.optimize is False
    assert f.netmask == 1


def test_detector_constructor():
    # we can construct alarm detectors
    d = Detector()
    assert d.filters == ()
    assert d.severity == 0
    assert d.tags == []
    assert d.message is None


def test_detector_finds_filter_matches():
    # we can get a list of filters matching a file
    f1 = Filter("dst 4.3.2.1")
    f2 = Filter("dst 8.8.8.8")
    d = Detector((f1, f2))
    path = os.path.join(SAMPLES_PATH, "single_ip.pcap")
    result = d.matching_filters(path)
    assert f1 in result
    assert f2 not in result
