from typing import Protocol, Any


class RepositoryProvider(Protocol):
    """Generic protocol for repository activity providers."""

    def fetch_events(self, username: str) -> list[dict[str, Any]]:
        """Retrieve public activity events for a given username."""

    def summarize_events(self, events: list[dict[str, Any]]) -> dict[tuple[str, str], int]:
        """Group or summarize events by type and repo name."""
