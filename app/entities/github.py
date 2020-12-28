import datetime

from pydantic import BaseModel


class GithubAuthorEvent(BaseModel):
    username: str


class GithubCommitEvent(BaseModel):
    id: str
    url: str
    message: str
    author: GithubAuthorEvent
    timestamp: datetime.datetime


class GithubPushEvent(BaseModel):
    commits: list[GithubCommitEvent] = []
