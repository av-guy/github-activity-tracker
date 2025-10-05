from typing import Protocol, Any


class Cache(Protocol):
    def cache_json_response(self, username: str, data: list[dict[str, Any]]) -> None:
        ...

    def get_json_response(self, username: str) -> list[dict[str, Any]] | None:
        ...

    def cache_events(self, username: str, summary: dict[tuple[str, str], int]) -> None:
        ...

    def get_events(self, username: str) -> dict[tuple[str, str], int] | None:
        ...
