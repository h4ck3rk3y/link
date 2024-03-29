DEFAULT_PAGE_SIZE = 15


# CATEGORIES OF RESULTS
QUESTION = "question"
ISSUE = "issue"
CODE = "code"
REPO = "repository"
MESSAGE = "message"
MERGE_REQUESTS = "merge_requests"
FILE = "file"
FOLDER = "folder"
WEB_LINK = "web_link"


# Trello
CARDS = "cards"
BOARDS = "boards"
ORGANIZATIONS = "organizations"
MEMBERS = "members"

# Task
TASK = "task"

# Jira
ISSUE = "issue"
WIKI = "wiki"

GITHUB_QUALIFIERS = set([
    "in:file",
    "in:path",
    "in:name",
    "in:description",
    "in:readme",
    "user",
    "org",
    "repo",
    "path",
    "size",
    "filename",
    "extension",
    "followers",
    "forks",
    "created",
    "pushed",
    "language",
    "topic",
    "topics",
    "license",
    "is:public",
    "is:private",
    "mirror:true",
    "mirror:false",
    "good-first-issues",
    "help-wanted-issues",
    "is:curated",
    "is:featured",
    "is:not-curated",
    "is:not-featured",
    "repositories",
    "author",
    "committer",
    "author-name",
    "committer-name",
    "author-email",
    "committer-email",
    "author-date",
    "committer-date",
    "merge:true",
    "merge:false",
    "hash",
    "parent",
    "tree",
    "type:pr",
    "type:issue",
    "is:pr",
    "is:issue",
    "in:title",
    "in:body",
    "in:comments",
    "state:open",
    "state:closed",
    "is:open",
    "is:closed",
    "assignee",
    "mentions",
    "team",
    "commenter",
    "involves",
    "linked:pr",
    "linked:issue",
    "-linked:pr",
    "-linked:issue",
    "label:LABEL",
    "milestone",
    "project",
    "status:pending",
    "status:success",
    "status:failure",
    "head",
    "base",
    "comments",
    "interactions",
    "reactions",
    "draft:true",
    "draft:false",
    "review:none",
    "review:required",
    "review:approved",
    "review:changes_requested",
    "reviewed-by",
    "review-requested",
    "team-review-requested",
    "updated",
    "closed",
    "merged",
    "is:merged",
    "is:unmerged",
    "archived:true",
    "archived:false",
    "is:locked",
    "is:unlocked",
    "no:label",
    "no:milestone",
    "no:assignee",
    "no:project",
    "type:user",
    "type:org",
    "in:login",
    "fullname:",
    "in:email",
    "repos",
    "location",
    "fork:only",
    "fork:true",
])


GITHUB_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
BOX_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TRELLO_GITLAB_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
MICROSOFT_TIME_FORMAT = TRELLO_GITLAB_TIME_FORMAT
ATLASSIAN_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
