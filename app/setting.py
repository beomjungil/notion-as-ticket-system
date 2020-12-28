from typing import Dict

from notion.client import NotionClient
from yaml import load, FullLoader

import app.core.notion_client as notion_client
from app.entities.project import Project

with open('setting.yaml') as file:
    __setting_map__ = load(file, Loader=FullLoader)
    notion_base_url = 'https://notion.so/'
    notion_client = notion_client.init(token=__setting_map__.get('notion_token'))
    projects: Dict[str, Project] = {
        project_map.get('project_prefix'): Project(
            **project_map,
            collection_view=notion_client.get_collection_view(
                project_map.get('notion_board_url')
            )
        ) for project_map in __setting_map__.get('projects')
    }
