from fastapi import HTTPException

from app import setting
from app.entities.project import Project


def get_notion_project(prefix_id: str) -> Project:
    project = setting.projects.get(prefix_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
