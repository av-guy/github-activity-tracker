# GitHub Activity CLI

A simple command-line tool that fetches and summarizes a user's public GitHub activity, with optional caching and event filtering.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/av-guy/github-activity-tracker.git
cd github-activity-tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows use: .venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Show available commands and options:

```bash
python -m activity-tracker --help
```

Run the tool for a GitHub username:

```bash
python -m activity-tracker <username>
```

By default, results are cached between runs.

Use `--no-cache` to bypass the cache, or `--filter` to show only specific event types (for example, PushEvent or PullRequestEvent).

Example:

```bash
python -m activity-tracker <username> --filter pullrequestevent
```
