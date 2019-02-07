import os
import pytest
import sys
from scapy.all import sniff
from sb_finder import matches_filter, Filter, Detector, main, handle_options

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


class TestHandleOptions(object):

    def test_handle_options(self, capsys):
        # we can get help
        with pytest.raises(SystemExit) as exc_info:
            handle_options(["p", '--help'])
        out, err = capsys.readouterr()
        assert exc_info.value.code == 0
        assert 'usage: ' in out

    def test_filename(self):
        # we can get any passed in filename
        args = handle_options(["-f", "somepath"])
        assert args.file == "somepath"
        args = handle_options(["--file", "otherpath"])
        assert args.file == "otherpath"


def test_main_requires_file(capsys):
    # a file is required to run main
    with pytest.raises(SystemExit) as exc_info:
        main([])
    out, err = capsys.readouterr()
    if sys.version_info < (3, 0):
        assert "argument -f/--file is required" in err
    else:
        assert "the following arguments are required: -f" in err
    assert out == ""
    assert exc_info.value.code == 2


def test_main_argv(argv_handler):
    # main() handles sys.argv if nothing is provided
    sys.argv = ['sb_finder', '--help']
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
