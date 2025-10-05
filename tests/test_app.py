# pylint: disable=import-outside-toplevel

from unittest.mock import MagicMock
from typer.testing import CliRunner
from kink import di

from activity_tracker.__main__ import app
from activity_tracker.providers.github import EventsProvider, GitHub
from activity_tracker.caches.in_memory import CacheProvider, InMemory

runner = CliRunner()


def test_main_command_with_mocked_dependencies():
    mock_provider = MagicMock()
    mock_cache = MagicMock()

    mock_provider.provider.fetch_events.return_value = [{"id": 1, "type": "PushEvent"}]
    mock_provider.provider.summarize_events.return_value = {("PushEvent", "repo1"): 2}

    mock_cache.cache.cache_expired.return_value = True
    mock_cache.cache.get_json_response.return_value = [{"id": 1, "type": "PushEvent"}]
    mock_cache.cache.get_events.return_value = {("PushEvent", "repo1"): 2}

    di[EventsProvider[GitHub]] = mock_provider
    di[CacheProvider[InMemory]] = mock_cache

    result = runner.invoke(app, ["un", "--no-cache"])

    assert result.exit_code == 0
    assert "- Pushed 2 commits to repo1" in result.output

    mock_provider.provider.fetch_events.assert_called_once_with("un")
    mock_cache.cache.cache_json_response.assert_called_once()
    mock_cache.cache.cache_events.assert_called_once()
    mock_cache.cache.save.assert_called_once()


def test_main_command_handles_http_error(monkeypatch):
    mock_provider = MagicMock()
    mock_cache = MagicMock()

    from requests.exceptions import HTTPError
    mock_provider.provider.fetch_events.side_effect = HTTPError("API error")

    di[EventsProvider[GitHub]] = mock_provider
    di[CacheProvider[InMemory]] = mock_cache

    from activity_tracker.activities.summary import ActivitySummary
    monkeypatch.setattr(ActivitySummary, "display_summary", lambda self: None)

    result = runner.invoke(app, ["un", "--no-cache"])

    assert result.exit_code == 0
    assert "API error" in result.output
