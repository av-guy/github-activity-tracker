from typing import Any
from requests.exceptions import HTTPError

from ..protocols.provider import RepositoryProvider
from .descriptors import EVENT_DESCRIPTORS, EventDescriptor


class ActivitySummary:
    def __init__(self, username: str, provider: RepositoryProvider):
        self.username = username
        self.provider = provider

        self.events: list[dict[str, Any]] = []
        self.event_groups: dict[tuple[str, str], int] = {}

    def run(self):
        try:
            self.events = self.provider.fetch_events(self.username)
            self.event_groups = self.provider.summarize_events(self.events)

            self.display_summary()
        except HTTPError as exc:
            print(exc)

    def display_summary(self):
        print("Activity Summary:\n")

        for (event_type, repo_name), count in sorted(
            self.event_groups.items(), key=lambda x: x[0][1].lower()
        ):
            descriptor = EVENT_DESCRIPTORS.get(
                event_type, EventDescriptor(
                    "Performed", "action", "actions", "on")
            )
            noun = descriptor.plural if count > 1 else descriptor.singular
            connector = f" {descriptor.target}" if descriptor.target else ""
            print(f"- {descriptor.verb} {count} {noun}{connector} {repo_name}")

        print("\nDone.")
