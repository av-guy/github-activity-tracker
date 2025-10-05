from pickle import dump, load, UnpicklingError
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Generic, TypeVar

from ..protocols.cache import Cache

P = TypeVar("P", bound=Cache)


class CacheProvider(Generic[P]):
    def __init__(self, cache: P):
        self.cache = cache


class InMemory:
    CACHE_FILE = Path(".cache.pkl")
    EXPIRATION_MINUTES = 30

    def __init__(self):
        self._json_cache: dict[str, list[dict[str, Any]]] = {}
        self._events_cache: dict[str, dict[tuple[str, str], int]] = {}
        self._expiration: datetime = datetime.now()
        self._load_from_disk()

    def cache_expired(self) -> bool:
        return datetime.now() >= self._expiration

    def reset_cache_timer(self) -> None:
        self._expiration = datetime.now() + timedelta(minutes=self.EXPIRATION_MINUTES)

    def cache_json_response(self, username: str, data: list[dict[str, Any]]) -> None:
        self._json_cache[username] = data

    def get_json_response(self, username: str) -> list[dict[str, Any]] | None:
        return self._json_cache.get(username)

    def cache_events(self, username: str, summary: dict[tuple[str, str], int]) -> None:
        self._events_cache[username] = summary

    def get_events(self, username: str) -> dict[tuple[str, str], int] | None:
        return self._events_cache.get(username)

    def save(self) -> None:
        data = {
            "json_cache": self._json_cache,
            "events_cache": self._events_cache,
            "expiration": self._expiration,
        }

        with open(self.CACHE_FILE, "wb") as f:
            dump(data, f)

    def _load_from_disk(self) -> None:
        if not self.CACHE_FILE.exists():
            return

        try:
            with open(self.CACHE_FILE, "rb") as f:
                data = load(f)

            if not isinstance(data, dict):
                raise ValueError("Cache file format invalid (expected dict)")

            self._json_cache = data.get("json_cache", {})
            self._events_cache = data.get("events_cache", {})
            self._expiration = data.get("expiration", datetime.now())

        except (OSError, EOFError, UnpicklingError) as e:
            print(f"[Cache] Could not read cache file: {e}. Starting fresh.")
            self._reset()
        except ValueError as e:
            print(f"[Cache] Invalid cache contents: {e}. Starting fresh.")
            self._reset()

    def _reset(self) -> None:
        self._json_cache = {}
        self._events_cache = {}
        self._expiration = datetime.now()
