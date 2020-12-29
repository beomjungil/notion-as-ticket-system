import datetime
from typing import Optional, List

from pydantic import BaseModel


class GithubAuthor(BaseModel):
    username: str


class GithubCommit(BaseModel):
    id: str
    url: str
    message: str
    author: GithubAuthor
    timestamp: datetime.datetime


class GithubPullRequestUser(BaseModel):
    login: str


class GithubPullRequest(BaseModel):
    title: str
    html_url: str
    user: GithubPullRequestUser
    created_at: datetime.datetime
    merged_at: datetime.datetime
    body: str


class GithubPullRequestBranch(BaseModel):
    ref: str


class GithubEvent(BaseModel):
    action: Optional[str]
    pull_request: Optional[GithubPullRequest]
    base: Optional[GithubPullRequestBranch]
    head: Optional[GithubPullRequestBranch]
    commits: Optional[List[GithubCommit]] = []
