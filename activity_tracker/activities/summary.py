from typing import Any
from requests.exceptions import HTTPError

from ..protocols.events import Events
from ..protocols.cache import Cache

from .descriptors import EVENT_DESCRIPTORS, EventDescriptor, GitHubEvents


class ActivitySummary:
    def __init__(
        self,
        username: str,
        provider: Events,
        cache: Cache,
        event_filter: GitHubEvents | None = None
    ):
        self.user_name = username
        self.provider = provider
        self.cache = cache
        self.event_filter = event_filter
        self.events: list[dict[str, Any]] = []
        self.event_groups: dict[tuple[str, str], int] = {}

    def run(self, no_cache: bool = False):
        if no_cache or self.cache.cache_expired():
            json_response = self.provider.fetch_events(self.user_name)
            event_groups = self.provider.summarize_events(json_response)

            self.cache.cache_json_response(self.user_name, json_response)
            self.cache.cache_events(self.user_name, event_groups)
            self.cache.reset_cache_timer()
            self.cache.save()

        self.events = self.cache.get_json_response(self.user_name)
        self.event_groups = self.cache.get_events(self.user_name)

        if self.event_filter is not None:
            filtered_groups = {
                (event_type, repo): count
                for (event_type, repo), count in self.event_groups.items()
                if event_type.split(":")[0] == self.event_filter.value
            }
            self.event_groups = filtered_groups

        self.display_summary()


    def display_summary(self):
        print("")

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

        print("")
