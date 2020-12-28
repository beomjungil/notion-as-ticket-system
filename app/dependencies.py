from fastapi import HTTPException

from app import setting


async def get_project_by_prefix(prefix_id: str):
    project = setting.projects.get(prefix_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
