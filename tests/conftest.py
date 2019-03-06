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
def path_dir(request, monkeypatch, tmpdir):
    """A fixture extending the $PATH.

    Returns the newly generated path. It will be torn down after any testing.
    """
    new_path = [str(tmpdir)] + sys.path
    monkeypatch.setattr(sys, "path", new_path)
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
