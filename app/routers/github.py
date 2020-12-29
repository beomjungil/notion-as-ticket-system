from typing import Optional, List

from fastapi import APIRouter, Depends, Header
import re

from notion.collection import CollectionRowBlock

from app.core.expections import NotionException
from app.dependencies import get_project_by_prefix
from app.entities.project import Project
from app.setting import notion_client
from app.entities.github import GithubEvent, GithubCommit, GithubPullRequest

router = APIRouter(prefix="/github")

ticket_regex = re.compile("([A-Z]{3})-([0-9]+)")

close_ticket_regex = re.compile(
    r"\b(?:[Cc]los(?:e[sd]?|ing)|\b[Ff]ix(?:e[sd]|ing)?|\b[Rr]esolv(?:e[sd]?|ing)|\b[Ii]mplement(?:s|ed|ing)?):? ([A-Z]{3})-([0-9]+)"
)


@router.post("/{prefix_id}/webhook")
def github_webhook(
    github_event: GithubEvent,
    x_github_event: Optional[str] = Header(None),
    project: Project = Depends(get_project_by_prefix),
):
    if x_github_event == "push":
        add_commit_comment(project=project, commits=github_event.commits)
        close_with_commit(project=project, commits=github_event.commits)
    elif x_github_event == "pull_request":
        if github_event.action == "opened":
            add_pr_comment(project=project, pull_request=github_event.pull_request)
        if github_event.action == "closed" and github_event.pull_request.merged_at is not None:
            close_with_pr(project=project, pull_request=github_event.pull_request)

    return {"result": "ok"}


def add_commit_comment(project: Project, commits: List[GithubCommit]):
    for commit in commits:
        result = ticket_regex.search(commit.message)
        if result is not None:
            ticket_id = result.groups()[1]
            try:
                ticket = project.query_ticket(ticket_id=ticket_id)
                commit_message = re.sub(ticket_regex, "", commit.message).splitlines()[0].strip()
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
                continue


def add_pr_comment(project: Project, pull_request: GithubPullRequest):
    result = ticket_regex.search(pull_request.title)
    if result is not None:
        ticket_id = result.groups()[1]
        try:
            pr_title = re.sub(ticket_regex, "", pull_request.title).strip()
            ticket = project.query_ticket(ticket_id=ticket_id)
            notion_client.comment(
                notion_client,
                page_id=ticket.id,
                tag_body="PR Open",
                tag_link=pull_request.html_url,
                body=pr_title,
                author=pull_request.user.login,
                timestamp=pull_request.created_at.timestamp() * 1000,
            )
        except NotionException:
            pass


def close_with_pr(project: Project, pull_request: GithubPullRequest):
    for bodyline in pull_request.body.splitlines():
        result = close_ticket_regex.search(bodyline)
        print(result)
        if result is not None:
            ticket_id = result.groups()[1]
            try:
                pr_title = re.sub(ticket_regex, "", pull_request.title).strip()
                ticket = project.query_ticket(ticket_id=ticket_id)
                close_ticket(project=project, ticket=ticket)
                notion_client.comment(
                    notion_client,
                    page_id=ticket.id,
                    tag_body="PR Close",
                    tag_link=pull_request.html_url,
                    body=pr_title,
                    author=pull_request.user.login,
                    timestamp=pull_request.created_at.timestamp() * 1000,
                )
            except NotionException:
                continue


def close_with_commit(project: Project, commits: List[GithubCommit]):
    for commit in commits:
        result = close_ticket_regex.search(commit.message.replace('\n', ' ').replace('\r', ''))
        if result is not None:
            ticket_id = result.groups()[1]
            try:
                ticket = project.query_ticket(ticket_id=ticket_id)
                close_ticket(project=project, ticket=ticket)
            except NotionException:
                continue


def close_ticket(project: Project, ticket: CollectionRowBlock):
    ticket.set_property(project.notion_status_property, project.notion_closed_status)
