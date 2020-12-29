from typing import Optional, List

from fastapi import APIRouter, Depends, Header
import re

from app.core.expections import NotionException
from app.dependencies import get_project_by_prefix
from app.entities.project import Project
from app.setting import notion_client
from app.entities.github import GithubEvent, GithubCommit

router = APIRouter(prefix="/github")

ticket_regex = re.compile("^([A-Z]+)-([0-9]+)")


@router.post("/{prefix_id}/webhook")
def github_webhook(
    github_event: GithubEvent,
    x_github_event: Optional[str] = Header(None),
    project: Project = Depends(get_project_by_prefix),
):
    if x_github_event == "push":
        add_commit_comment(project=project, commits=github_event.commits)
    elif x_github_event == "pull_request":
        print(github_event.action)
        print(github_event.pull_request)
        add_pr_comment(project=project, event=github_event)

    return {"result": "ok"}


def add_commit_comment(project: Project, commits: List[GithubCommit]):
    for commit in commits:
        result = ticket_regex.search(commit.message)
        if result is not None:
            ticket_id = result.groups()[1]
            try:
                ticket = project.query_ticket(ticket_id=ticket_id)
                commit_message = re.sub(ticket_regex, "", commit.message).strip()
                notion_client.comment(
                    notion_client,
                    page_id=ticket.id,
                    tag_body=commit.id[:7],
                    tag_link=commit.url,
                    body=commit_message,
                    author=commit.author.username,
                    timestamp=commit.timestamp.timestamp() * 1000,
                )
            except NotionException:
                return


def add_pr_comment(project: Project, event: GithubEvent):
    if event.action == "opened":
        result = ticket_regex.search(event.pull_request.title)
        if result is not None:
            ticket_id = result.groups()[1]
            try:
                pr_title = re.sub(ticket_regex, "", event.pull_request.title).strip()
                ticket = project.query_ticket(ticket_id=ticket_id)
                notion_client.comment(
                    notion_client,
                    page_id=ticket.id,
                    tag_body="PR Open",
                    tag_link=event.pull_request.html_url,
                    body=pr_title,
                    author=event.pull_request.user.login,
                    timestamp=event.pull_request.created_at.timestamp() * 1000,
                )
            except NotionException:
                return
