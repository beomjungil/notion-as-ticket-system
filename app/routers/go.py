from fastapi import APIRouter
from starlette.responses import RedirectResponse

from app.core.notion_helper import get_notion_project
import app.setting as setting
from app.core.expections import NotionException

router = APIRouter(
    prefix='/go'
)


@router.get('/{prefix_id}')
def redirect_to_board(prefix_id: str):
    project = get_notion_project(prefix_id=prefix_id)
    return RedirectResponse(url=project.notion_board_url)


@router.get('/{prefix_id}/{ticket_id}')
def redirect_to_board(prefix_id: str, ticket_id: str):
    project = get_notion_project(prefix_id=prefix_id)

    try:
        ticket = project.query_ticket(ticket_id=ticket_id)
        notion_url = setting.notion_base_url + ticket.id.replace('-', "")
        return RedirectResponse(url=notion_url)
    except NotionException:
        return RedirectResponse(url=project.notion_board_url)
