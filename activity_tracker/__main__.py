from typer import Typer
from .activities.summary import ActivitySummary
from .providers.github import GitHubProvider

app = Typer()


@app.command()
def main(user_name: str):
    github_provider = GitHubProvider()
    activity_summary = ActivitySummary(user_name, github_provider)

    activity_summary.run()


if __name__ == "__main__":
    app()
