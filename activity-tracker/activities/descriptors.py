from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class EventDescriptor:
    verb: str
    singular: str
    plural: str
    target: str


class GitHubEvents(str, Enum):
    PushEvent = "PushEvent"
    CreateEvent = "CreateEvent"
    DeleteEvent = "DeleteEvent"
    ForkEvent = "ForkEvent"
    WatchEvent = "WatchEvent"
    PublicEvent = "PublicEvent"
    IssuesEvent = "IssuesEvent"
    IssueCommentEvent = "IssueCommentEvent"
    PullRequestEvent = "PullRequestEvent"
    PullRequestReviewEvent = "PullRequestReviewEvent"
    PullRequestReviewCommentEvent = "PullRequestReviewCommentEvent"
    ReleaseEvent = "ReleaseEvent"
    MemberEvent = "MemberEvent"
    GollumEvent = "GollumEvent"


EVENT_DESCRIPTORS: dict[str, EventDescriptor] = {
    "PushEvent": EventDescriptor("Pushed", "commit", "commits", "to"),
    "CreateEvent:branch": EventDescriptor("Created", "branch", "branches", "in"),
    "CreateEvent:tag": EventDescriptor("Created", "tag", "tags", "in"),
    "CreateEvent:repository": EventDescriptor("Created", "repository", "repositories", ""),
    "DeleteEvent": EventDescriptor("Deleted", "branch/tag", "branches/tags", "in"),
    "ForkEvent": EventDescriptor("Forked", "repository", "repositories", ""),
    "WatchEvent": EventDescriptor("Starred", "repository", "repositories", ""),
    "PublicEvent": EventDescriptor("Made", "repository public", "repositories public", ""),
    "IssuesEvent": EventDescriptor("Opened or updated", "issue", "issues", "in"),
    "IssuesEvent:opened": EventDescriptor("Opened", "issue", "issues", "in"),
    "IssuesEvent:edited": EventDescriptor("Edited", "issue", "issues", "in"),
    "IssuesEvent:closed": EventDescriptor("Closed", "issue", "issues", "in"),
    "IssuesEvent:reopened": EventDescriptor("Reopened", "issue", "issues", "in"),
    "IssuesEvent:assigned": EventDescriptor("Assigned", "issue", "issues", "in"),
    "IssuesEvent:unassigned": EventDescriptor("Unassigned", "issue", "issues", "in"),
    "IssuesEvent:labeled": EventDescriptor("Labeled", "issue", "issues", "in"),
    "IssuesEvent:unlabeled": EventDescriptor("Unlabeled", "issue", "issues", "in"),
    "IssueCommentEvent:created": EventDescriptor("Created", "comment", "comments", "in"),
    "IssueCommentEvent:edited": EventDescriptor("Edited", "comment", "comments", "in"),
    "IssueCommentEvent:deleted": EventDescriptor("Deleted", "comment", "comments", "in"),
    "IssueCommentEvent": EventDescriptor("Commented on", "comment", "comments", "in"),
    "PullRequestEvent:opened": EventDescriptor("Opened", "pull request", "pull requests", "in"),
    "PullRequestEvent:edited": EventDescriptor("Edited", "pull request", "pull requests", "in"),
    "PullRequestEvent:closed": EventDescriptor("Closed", "pull request", "pull requests", "in"),
    "PullRequestEvent:reopened": EventDescriptor("Reopened", "pull request", "pull requests", "in"),
    "PullRequestEvent:assigned": EventDescriptor("Assigned", "pull request", "pull requests", "in"),
    "PullRequestEvent:unassigned": EventDescriptor(
        "Unassigned", "pull request", "pull requests", "in"),
    "PullRequestEvent:review_requested": EventDescriptor(
        "Requested review for", "pull request", "pull requests", "in"),
    "PullRequestEvent:review_request_removed": EventDescriptor(
        "Removed review request for", "pull request", "pull requests", "in"),
    "PullRequestEvent:labeled": EventDescriptor("Labeled", "pull request", "pull requests", "in"),
    "PullRequestEvent:unlabeled": EventDescriptor(
        "Unlabeled", "pull request", "pull requests", "in"),
    "PullRequestEvent:synchronize": EventDescriptor(
        "Synchronized", "pull request", "pull requests", "in"),
    "PullRequestEvent": EventDescriptor("Opened or merged", "pull request", "pull requests", "in"),
    "PullRequestReviewEvent": EventDescriptor("Reviewed", "pull request", "pull requests", "in"),
    "PullRequestReviewCommentEvent": EventDescriptor(
        "Commented on", "pull request", "pull requests", "in"),
    "ReleaseEvent": EventDescriptor("Published", "release", "releases", "in"),
    "MemberEvent": EventDescriptor(
        "Modified", "collaborator permission", "collaborator permissions", "on"),
    "GollumEvent": EventDescriptor("Edited", "wiki page", "wiki pages", "in")
}
