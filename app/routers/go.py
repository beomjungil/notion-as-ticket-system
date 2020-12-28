from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

import app.setting as setting
from app.core.expections import NotionException
from app.dependencies import get_project_by_prefix
from app.entities.project import Project
import json

router = APIRouter(
    prefix="/go",
)


@router.get("/{prefix_id}")
def redirect_to_board(project: Project = Depends(get_project_by_prefix)):
    return RedirectResponse(url=project.notion_board_url)


@router.get("/{prefix_id}/{ticket_id}")
def redirect_to_ticket(
    ticket_id: str, project: Project = Depends(get_project_by_prefix)
):
    try:
        ticket = project.query_ticket(ticket_id=ticket_id)
        notion_url = setting.notion_base_url + ticket.id.replace("-", "")
        return RedirectResponse(url=notion_url)
    except NotionException:
        return RedirectResponse(url=project.notion_board_url)
