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
    new_path = [str(tmpdir)] + sys.path
    monkeypatch.setattr(sys, "path", new_path)
    return str(tmpdir)
