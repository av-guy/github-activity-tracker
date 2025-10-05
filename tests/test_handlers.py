from pytest import mark

from activity_tracker.providers.handlers import (
    handle_push_event,
    handle_issue_comment_event,
    handle_create_event,
    handle_default_event,
    handle_issues_event,
    handle_pull_request_event,
)


def test_handle_push_event_with_multiple_commits():
    event = {
        "repo": {"name": "example/repo"},
        "payload": {"commits": [{"id": 1}, {"id": 2}, {"id": 3}]},
    }

    key, repo, count = handle_push_event(event)
    assert key == "PushEvent"
    assert repo == "example/repo"
    assert count == 3


def test_handle_push_event_with_non_list_commits_defaults_to_one():
    event = {
        "repo": {"name": "example/repo"},
        "payload": {"commits": "notalist"},
    }

    key, repo, count = handle_push_event(event)
    assert key == "PushEvent"
    assert repo == "example/repo"
    assert count == 1


def test_handle_issue_comment_event_builds_key_correctly():
    event = {
        "repo": {"name": "repo1"},
        "payload": {"action": "created"},
    }

    key, repo, count = handle_issue_comment_event(event)
    assert key == "IssueCommentEvent:created"
    assert repo == "repo1"
    assert count == 1


def test_handle_create_event_includes_ref_type():
    event = {
        "repo": {"name": "repo2"},
        "payload": {"ref_type": "branch"},
    }

    key, repo, count = handle_create_event(event)
    assert key == "CreateEvent:branch"
    assert repo == "repo2"
    assert count == 1


def test_handle_default_event_uses_type_and_defaults():
    event = {"type": "WatchEvent", "repo": {"name": "r"}}
    key, repo, count = handle_default_event(event)
    assert key == "WatchEvent"
    assert repo == "r"
    assert count == 1


def test_handle_default_event_missing_fields_fallbacks():
    key, repo, count = handle_default_event({})
    assert key == "UnknownEvent"
    assert repo == "Unknown Repo"
    assert count == 1


def test_handle_issues_event_includes_action():
    event = {
        "repo": {"name": "repo3"},
        "payload": {"action": "closed"},
    }

    key, repo, count = handle_issues_event(event)
    assert key == "IssuesEvent:closed"
    assert repo == "repo3"
    assert count == 1


def test_handle_pull_request_event_includes_action():
    event = {
        "repo": {"name": "repo4"},
        "payload": {"action": "opened"},
    }

    key, repo, count = handle_pull_request_event(event)
    assert key == "PullRequestEvent:opened"
    assert repo == "repo4"
    assert count == 1


@mark.parametrize(
    "handler",
    [
        handle_push_event,
        handle_issue_comment_event,
        handle_create_event,
        handle_issues_event,
        handle_pull_request_event,
    ],
)
def test_handlers_fallback_to_defaults_on_missing_fields(handler):
    key, repo, count = handler({})
    assert repo == "Unknown Repo"
    assert count == 1
    assert isinstance(key, str)
