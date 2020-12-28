from fastapi import APIRouter
import re

from app.core.expections import NotionException
from app.setting import notion_client
from app.core.notion_helper import get_notion_project
from app.entities.github import GithubPushEvent

router = APIRouter(
    prefix='/github'
)

ticket_commit_regex = re.compile('^([A-Z]+)-([0-9]+)')


@router.post('/webhook')
def github_webhook(push_event: GithubPushEvent):
    for commit in push_event.commits:
        result = ticket_commit_regex.search(commit.message)
        if result is not None:
            [project_prefix, ticket_id] = result.groups()
            project = get_notion_project(prefix_id=project_prefix)
            try:
                # TODO: Should find comment parent with ticket_id
                # ticket = project.query_ticket(ticket_id=ticket_id)
                commit_message = re.sub(ticket_commit_regex, '', commit.message)
                notion_client.comment(
                    notion_client,
                    tag_message=commit.id[:7],
                    tag_link=commit.url,
                    message=f'{commit_message} - {commit.author.username}',
                    timestamp=commit.timestamp.timestamp(),
                )
            except NotionException:
                return

    return {"result": "ok"}
