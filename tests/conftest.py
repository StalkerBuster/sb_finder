import os
import pytest
import sys


@pytest.fixture(scope="function")
def argv_handler(request):
    """This fixture restores sys.argv and sys.stdin after tests.
    """
    _argv_stored = sys.argv
    _stdin_stored = sys.stdin

    def teardown():
        sys.argv = _argv_stored
        sys.stdin = _stdin_stored
    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def path_dir(monkeypatch, tmpdir):
    """A fixture extending the $PATH.

    Returns the newly generated path. It will be torn down after any testing.
    """
    path = "%s:%s" % (tmpdir, os.getenv("PATH"))
    monkeypatch.setenv("PATH", path)
    return tmpdir


@pytest.fixture(scope="function")
def fake_ifconfig(path_dir):
    """Fixture to install fake ifconfig in new path.

    The path is prepended to $PATH, so that the newly installed version of
    `ifconfig` should be called instead of the system ones.
    """
    src_path = os.path.join(os.path.dirname(__file__), 'fake-ifconfig.sh')
    script_path = path_dir.join("ifconfig")
    script_path.write(open(src_path, "r").read())
    os.chmod(str(script_path), 0o744)
    return script_path


class FakeIwgetidCreator(object):
    """Create an executable iwgetid script.i

    The wireless tool `iwgetid` returns the current activated wireless lan. We
    simulate it with a simple script, which returns any desired SSID or exits
    with status -1 (in case no SSID is set).
    """
    def __init__(self, dst_path):
        self.dst = dst_path
        self.create_script()

    def create_script(self, ssid=None):
        if ssid is None:
            self.dst.write("#!/bin/bash\nexit -1\n")
        else:
            self.dst.write("#!/bin/bash\necho '%s'\nexit 0\n" % ssid)
        self.dst.chmod(0o744)


@pytest.fixture(scope="function")
def fake_iwgetid(path_dir):
    """Fixture to install fake iwgetid in new path.

    The path is prepended to $PATH, so that the newly installed version of
    `iwgetid` should be called instead of the system ones.

    Returns a function you can call to set any fake SSID. Call this function
    with no or the `None` argument, to simluate deactivated wifi.
    """
    script_path = path_dir.join("iwgetid")
    fake_iwgetid_creator = FakeIwgetidCreator(script_path)
    return fake_iwgetid_creator.create_script
