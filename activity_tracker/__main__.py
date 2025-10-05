from typing import Annotated
from typer import Typer, Argument, Option
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
def main(user_name: USER_NAME_ARGUMENT, cache: NO_CACHE_ARGUMENT = False):
    github_provider: EventsProvider[GitHub] = di[EventsProvider[GitHub]]
    cache_provider: CacheProvider[InMemory] = di[CacheProvider[InMemory]]

    if cache:
        print("Should not cache")

    activity_summary = ActivitySummary(user_name, github_provider.provider)
    activity_summary.run()


if __name__ == "__main__":
    bootstrap.initialize()
    app()
