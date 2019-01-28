import os
from scapy.all import sniff
from sb_finder import matches_filter, Filter, Detector, main

SAMPLES_PATH = os.path.abspath(os.path.dirname(__file__))
SAMPLE_IP_PATH = os.path.join(SAMPLES_PATH, 'single_ip.pcap')
SAMPLE_ICMP_PATH = os.path.join(SAMPLES_PATH, 'single_icmp.pcap')


def test_matches_filter_detects_ip_packets():
    # we can detect certain simple packets.
    data = sniff(offline=SAMPLE_IP_PATH)[-1]
    assert matches_filter(data, "ip") is True
    assert matches_filter(data, "tcp") is False


def notest_matches_filter_detects_dst():
    # we can filter by destination ip
    data = sniff(offline=SAMPLE_IP_PATH)[-1]
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
    result = d.matching_filters(SAMPLE_IP_PATH)
    assert f1 in result
    assert f2 not in result


def test_main_requires_file_or_iface(capsys):
    # without any args we get a hint what is missing
    main([])
    out, err = capsys.readouterr()
    assert "file or interface required." in err
    assert out == ""
