from notion.collection import CollectionView, CollectionRowBlock

from app.core.expections import NotionException


class Project:
    def __init__(self, name, github_repo, notion_board_url, notion_ticket_id_property, project_prefix, collection_view,
                 *args, **kwargs):
        self.name: str = name
        self.github_repo: str = github_repo
        self.notion_board_url: str = notion_board_url
        self.notion_ticket_id_property: str = notion_ticket_id_property
        self.project_prefix: str = project_prefix
        self.collection_view: CollectionView = collection_view

    def query_ticket(self, ticket_id: str) -> CollectionRowBlock:
        filter_params = {
            "operator": "and",
            "filters": [
                {
                    "property": self.notion_ticket_id_property,
                    "filter": {
                        "operator": "string_is",
                        "value": {
                            "type": "exact",
                            "value": f'{self.project_prefix}-{ticket_id}'
                        }
                    }
                }
            ]
        }
        query_result = self.collection_view.build_query(filter=filter_params).execute()

        if len(query_result) == 1:
            return query_result[0]
        elif len(query_result) > 1:
            raise NotionException(message='Found more than one ticket')
        else:
            raise NotionException(message='No ticket')
