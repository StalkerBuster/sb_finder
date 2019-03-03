from utils import get_avail_netdevs, get_avail_wlans


def test_get_avail_netdevs():
    devs = get_avail_netdevs()
    assert "lo" in devs
    assert type(devs) == list
