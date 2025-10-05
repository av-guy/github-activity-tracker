from typing import Annotated
from typer import Typer, Argument, Option
from kink import di

from . import bootstrap

from .activities.summary import ActivitySummary
from .providers.github import Provider, GitHub

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
        '--no-cache'
        '--n',
        help="Set to bypass cached result."
    )
]


@app.command()
def main(user_name: str):
    github_provider: Provider[GitHub] = di[Provider[GitHub]]
    activity_summary = ActivitySummary(user_name, github_provider.provider)

    activity_summary.run()


if __name__ == "__main__":
    bootstrap.initialize()
    app()
