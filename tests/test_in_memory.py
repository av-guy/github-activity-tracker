# pylint: disable=protected-access

from datetime import datetime, timedelta

from pickle import load, dump
from pytest import fixture

from activity_tracker.caches.in_memory import InMemory


@fixture(autouse=True)
def cleanup_cache(tmp_path):
    InMemory.CACHE_FILE = tmp_path / ".cache.pkl"

    yield

    if InMemory.CACHE_FILE.exists():
        InMemory.CACHE_FILE.unlink()


def test_cache_json_and_events_storage():
    cache = InMemory()
    cache.cache_json_response("un", [{"id": 1}])
    cache.cache_events("un", {("PushEvent", "repo"): 3})

    assert cache.get_json_response("un") == [{"id": 1}]
    assert cache.get_events("un") == {("PushEvent", "repo"): 3}


def test_cache_expiration_and_reset():
    cache = InMemory()
    assert cache.cache_expired() is True

    cache.reset_cache_timer()
    assert cache.cache_expired() is False


def test_save_creates_and_persists_file(tmp_path):
    InMemory.CACHE_FILE = tmp_path / ".cache.pkl"

    cache = InMemory()

    cache.cache_json_response("un", [{"test": 1}])
    cache.cache_events("un", {("Event", "Repo"): 5})
    cache.reset_cache_timer()
    cache.save()

    assert InMemory.CACHE_FILE.exists()

    with open(InMemory.CACHE_FILE, "rb") as f:
        data = load(f)
        assert "json_cache" in data
        assert "events_cache" in data
        assert "expiration" in data


def test_load_from_disk_restores_data(tmp_path):
    path = tmp_path / ".cache.pkl"

    test_data = {
        "json_cache": {"un": [{"x": 1}]},
        "events_cache": {"un": {("A", "B"): 2}},
        "expiration": datetime.now() + timedelta(minutes=5),
    }

    with open(path, "wb") as f:
        dump(test_data, f)

    InMemory.CACHE_FILE = path
    cache = InMemory()

    assert cache.get_json_response("un") == [{"x": 1}]
    assert cache.get_events("un") == {("A", "B"): 2}
    assert not cache.cache_expired()


def test_load_from_disk_invalid_data_triggers_reset(tmp_path, capsys):
    path = tmp_path / ".cache.pkl"

    with open(path, "wb") as f:
        f.write(b"not a pickle")

    InMemory.CACHE_FILE = path
    cache = InMemory()
    out = capsys.readouterr().out

    assert "[Cache]" in out

    assert cache.get_json_response("un") == {}
    assert cache.get_events("un") == {}


def test_load_from_disk_with_non_dict_triggers_reset(tmp_path, capsys):
    path = tmp_path / ".cache.pkl"

    with open(path, "wb") as f:
        dump(["wrong_type"], f)

    InMemory.CACHE_FILE = path
    cache = InMemory()
    out = capsys.readouterr().out

    assert "Invalid cache contents" in out

    assert cache.get_json_response("un") == {}
    assert cache.get_events("un") == {}


def test_reset_clears_all_fields(tmp_path):
    path = tmp_path / ".cache.pkl"

    test_data = {
        "json_cache": {"un": [{"x": 1}]},
        "events_cache": {"un": {("A", "B"): 2}},
        "expiration": datetime.now() + timedelta(minutes=5),
    }

    with open(path, "wb") as f:
        dump(test_data, f)

    InMemory.CACHE_FILE = path
    cache = InMemory()

    cache._reset()

    assert cache.get_json_response("un") == {}
    assert cache.get_events("un") == {}
    assert cache.cache_expired() is True
