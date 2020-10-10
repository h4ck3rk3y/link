from .link_github_code import GithubCodeSearcher
from .link_github_issues import GithubIssueSearcher
from .link_github_repos import GithubRepoSearcher
from .link_gitlab_issues import GitlabIssueSearcher
from .link_gitlab_merge_requests import GitlabMergeRequestSearcher
from .link_gitlab_projects import GitlabProjectSearcher
from .link_slack import SlackSearcher
from .link_stackoverflow import StackoverflowSearcher
from .link_trello import TrelloSearcher
from .link_box import BoxSearcher


available_searchers = {
    "github": [
        GithubCodeSearcher, GithubIssueSearcher, GithubRepoSearcher
    ],
    "gitlab": [
        GitlabIssueSearcher, GitlabMergeRequestSearcher, GitlabProjectSearcher
    ],
    "slack": [
        SlackSearcher
    ],
    "trello": [
        TrelloSearcher
    ],
    "stackoverflow": [
        StackoverflowSearcher
    ],
    "box": [
        BoxSearcher
    ]
}
