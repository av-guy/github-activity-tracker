# pylint: disable=redefined-outer-name

from unittest.mock import MagicMock
from pytest import fixture, raises
from requests import HTTPError

from activity_tracker.activities.summary import ActivitySummary
from activity_tracker.activities.descriptors import GitHubEvents


@fixture
def mock_provider():
    provider = MagicMock()

    provider.fetch_events.return_value = [{"type": "PushEvent"}]
    provider.summarize_events.return_value = {("PushEvent", "repo1"): 2}

    return provider


@fixture
def mock_cache():
    cache = MagicMock()

    cache.cache_expired.return_value = True
    cache.get_json_response.return_value = [{"type": "PushEvent"}]
    cache.get_events.return_value = {("PushEvent", "repo1"): 2}

    return cache


def test_run_refreshes_cache_when_expired(mock_provider: MagicMock, mock_cache: MagicMock):
    summary = ActivitySummary("user_name", mock_provider, mock_cache)
    summary.run()

    mock_provider.fetch_events.assert_called_once_with("user_name")
    mock_cache.cache_json_response.assert_called_once()
    mock_cache.cache_events.assert_called_once()
    mock_cache.save.assert_called_once()


def test_run_uses_cached_data_when_not_expired(mock_provider, mock_cache):
    mock_cache.cache_expired.return_value = False
    summary = ActivitySummary("user_name", mock_provider, mock_cache)
    summary.run()

    mock_provider.fetch_events.assert_not_called()
    mock_cache.cache_json_response.assert_not_called()


def test_run_applies_event_filter(mock_provider, mock_cache):
    event_filter = GitHubEvents.PushEvent

    summary = ActivitySummary(
        "user_name", mock_provider, mock_cache, event_filter)
    summary.run()

    assert all(
        k[0].split(":")[0] == event_filter.value
        for k in summary.event_groups
    )


def test_run_handles_http_error_gracefully(mock_provider, mock_cache):
    mock_provider.fetch_events.side_effect = HTTPError("API error")
    summary = ActivitySummary("user_name", mock_provider, mock_cache)

    with raises(HTTPError):
        summary.run()


def test_display_summary_prints_output(capsys):
    event_groups = {("PushEvent", "repo1"): 3}

    summary = ActivitySummary("user_name", MagicMock(), MagicMock())
    summary.event_groups = event_groups
    summary.display_summary()

    captured = capsys.readouterr()
    assert "- Pushed 3 commits to repo1" in captured.out
