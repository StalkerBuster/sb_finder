import os
import subprocess
from utils import get_avail_netdevs


def test_get_avail_netdevs():
    # yes, we can get any network device name
    devs = get_avail_netdevs()
    assert "lo" in devs
    assert type(devs) == list


def test_get_avail_netdevs_can_extract_names(fake_ifconfig):
    # we can get an expected set of device names
    devs = get_avail_netdevs()
    assert "foobar0" in devs
    assert "lo" in devs
    assert "wlp1s0" in devs


def test_fake_ifconfig(fake_ifconfig):
    # ensure, the `fake_ifconfig` fixture works.
    lines = subprocess.check_output("ifconfig").decode("utf-8")
    assert os.path.exists(str(fake_ifconfig))
    assert "foobar0:" in lines
