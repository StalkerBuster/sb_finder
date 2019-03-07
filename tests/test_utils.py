import os
import subprocess
from utils import get_avail_netdevs, get_avail_wlans


def test_get_avail_netdevs():
    devs = get_avail_netdevs()
    assert "lo" in devs
    assert type(devs) == list


def test_fake_ifconfig(fake_ifconfig):
    # ensure, the `fake_ifconfig` fixture works.
    lines = subprocess.check_output("ifconfig").decode("utf-8")
    assert os.path.exists(str(fake_ifconfig))
    assert "foobar0:" in lines
