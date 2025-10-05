from typing import Annotated
from typer import Typer, Argument, Option
from rich.progress import Progress, SpinnerColumn, TextColumn
from kink import di

from . import bootstrap

from .activities.summary import ActivitySummary
from .activities.descriptors import GitHubEvents

from .providers.github import EventsProvider, GitHub
from .caches.in_memory import CacheProvider, InMemory

app = Typer()

USER_NAME_ARGUMENT = Annotated[
    str,
    Argument(
        help="The user's GitHub username."
    )
]

NO_CACHE_ARGUMENT = Annotated[
    bool,
    Option(
        '--no-cache',
        '-n',
        help="Bypass the cached result, resetting the in-memory cache."
    )
]

EVENTS_FILTER = Annotated[
    GitHubEvents,
    Option(
        "--filter",
        "-f",
        case_sensitive=False,
        help="The event type to use in the filter."
    )
]


@app.command()
def main(
    user_name: USER_NAME_ARGUMENT,
    no_cache: NO_CACHE_ARGUMENT = False,
    event_filter: EVENTS_FILTER = None
):
    github_provider: EventsProvider[GitHub] = di[EventsProvider[GitHub]]
    cache_provider: CacheProvider[InMemory] = di[CacheProvider[InMemory]]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(description="Retrieving Events...", total=None)

        activity_summary = ActivitySummary(
            user_name,
            github_provider.provider,
            cache=cache_provider.cache,
            event_filter=event_filter
        )

        activity_summary.run(no_cache=no_cache)


if __name__ == "__main__":
    bootstrap.initialize()
    app()
