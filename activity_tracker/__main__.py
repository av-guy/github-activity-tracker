from typing import Annotated
from typer import Typer, Argument, Option
from rich.progress import Progress, SpinnerColumn, TextColumn
from kink import di

from . import bootstrap

from .activities.summary import ActivitySummary
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


@app.command()
def main(user_name: USER_NAME_ARGUMENT, no_cache: NO_CACHE_ARGUMENT = False):
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
            cache=cache_provider.cache
        )

        activity_summary.run(no_cache=no_cache)


if __name__ == "__main__":
    bootstrap.initialize()
    app()
