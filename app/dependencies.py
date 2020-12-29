from app import setting
from app.core.expections import NotionException


async def get_project_by_prefix(prefix_id: str):
    project = setting.projects.get(prefix_id)
    if project is None:
        raise NotionException(
            code=prefix_id, is_ticket=False, redirect_to=setting.notion_base_url
        )
    return project
