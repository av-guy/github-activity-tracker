from typing import Any, Generic, TypeVar
from ..protocols.cache import Cache

P = TypeVar("P", bound=Cache)


class CacheProvider(Generic[P]):
    def __init__(self, cache: P):
        self.cache = cache


class InMemory:
    def __init__(self):
        self._json_cache: dict[str, list[dict[str, Any]]] = {}
        self._events_cache: dict[str, dict[tuple[str, str], int]] = {}

    def cache_json_response(self, username: str, data: list[dict[str, Any]]) -> None:
        self._json_cache[username] = data

    def get_json_response(self, username: str) -> list[dict[str, Any]] | None:
        return self._json_cache.get(username)

    def cache_events(self, username: str, summary: dict[tuple[str, str], int]) -> None:
        self._events_cache[username] = summary

    def get_events(self, username: str) -> dict[tuple[str, str], int] | None:
        return self._events_cache.get(username)
