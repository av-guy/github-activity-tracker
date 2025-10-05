from typing import Any


def handle_push_event(event: dict[str, Any]) -> tuple[str, str, int]:
    repo = event.get("repo", {}).get("name", "Unknown Repo")
    commits = event.get("payload", {}).get("commits", [])
    count = len(commits) if isinstance(commits, list) else 1
    return "PushEvent", repo, count


def handle_issue_comment_event(event: dict[str, Any]) -> tuple[str, str, int]:
    repo = event.get("repo", {}).get("name", "Unknown Repo")
    action = event.get("payload", {}).get("action", "unknown")
    key = f"IssueCommentEvent:{action}"
    return key, repo, 1


def handle_create_event(event: dict[str, Any]) -> tuple[str, str, int]:
    repo = event.get("repo", {}).get("name", "Unknown Repo")
    ref_type = event.get("payload", {}).get("ref_type", "unknown")
    key = f"CreateEvent:{ref_type}"
    return key, repo, 1


def handle_default_event(event: dict[str, Any]) -> tuple[str, str, int]:
    repo = event.get("repo", {}).get("name", "Unknown Repo")
    key = event.get("type", "UnknownEvent")
    return key, repo, 1


def handle_issues_event(event: dict[str, Any]) -> tuple[str, str, int]:
    repo = event.get("repo", {}).get("name", "Unknown Repo")
    action = event.get("payload", {}).get("action", "unknown")
    key = f"IssuesEvent:{action}"
    return key, repo, 1


def handle_pull_request_event(event: dict[str, Any]) -> tuple[str, str, int]:
    repo = event.get("repo", {}).get("name", "Unknown Repo")
    action = event.get("payload", {}).get("action", "unknown")
    key = f"PullRequestEvent:{action}"
    return key, repo, 1
