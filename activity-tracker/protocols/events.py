from typing import Protocol, Any


class Events(Protocol):
    def fetch_events(self, username: str) -> list[dict[str, Any]]:
        ...

    def summarize_events(self, events: list[dict[str, Any]]) -> dict[tuple[str, str], int]:
        ...
