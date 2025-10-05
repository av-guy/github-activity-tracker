from typing import Any, Callable, Generic, TypeVar
from collections import defaultdict
from requests import get

from .events import (
    handle_create_event,
    handle_default_event,
    handle_issue_comment_event,
    handle_push_event,
    handle_issues_event,
    handle_pull_request_event
)

from ..protocols.provider import RepositoryProvider

P = TypeVar("P", bound=RepositoryProvider)


class Provider(Generic[P]):
    def __init__(self, provider: P):
        self.provider = provider


class GitHub:
    API_URL_TEMPLATE = "https://api.github.com/users/{username}/events/public"
    HEADERS = {"Accept": "application/vnd.github+json"}

    _HANDLERS: dict[str, Callable[[dict[str, Any]], tuple[str, str, int]]] = {
        "PushEvent": handle_push_event,
        "IssueCommentEvent": handle_issue_comment_event,
        "CreateEvent": handle_create_event,
        "IssuesEvent": handle_issues_event,
        "PullRequestEvent": handle_pull_request_event,
    }

    def fetch_events(self, username: str) -> list[dict[str, Any]]:
        url = self.API_URL_TEMPLATE.format(username=username)
        response = get(url, headers=self.HEADERS, timeout=5.0)
        response.raise_for_status()

        return response.json()

    def summarize_events(self, events: list[dict[str, Any]]) -> dict[tuple[str, str], int]:
        groups: dict[tuple[str, str], int] = defaultdict(int)

        for event in events:
            event_type = event.get("type")
            handler = self._HANDLERS.get(event_type, handle_default_event)
            key, repo, count = handler(event)
            groups[(key, repo)] += count

        return groups
