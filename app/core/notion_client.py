from uuid import uuid1

from notion.client import NotionClient


def init(token: str) -> NotionClient:
    client = NotionClient(token_v2=token)
    client.comment = __comment__
    return client


def __comment__(self, tag_message: str, tag_link: str, message: str, timestamp: int) -> dict:
    new_request_id = str(uuid1())
    new_comment_id = str(uuid1())
    new_transaction_id = str(uuid1())
    # TODO: Hardcoded parent_id. should find correct parrent_id(Discussion Collect's id)
    # TODO: Should create Discussion Collection when no discussion
    parent_id = "366242d2-6d43-4643-b3de-a1d4c6bf0a3c"
    transaction = {
        "requestId": new_request_id,
        "transactions": [
            {
                "id": new_transaction_id,
                "spaceId": "15c95d23-c4d5-436e-aa3a-1acbc7f7876c",
                "operations": [
                    {
                        "id": new_comment_id,
                        "table": "comment",
                        "path": [],
                        "command": "set",
                        "args": {
                            "parent_id": parent_id,
                            "parent_table": "discussion",
                            "text": [
                                [
                                    tag_message,
                                    [
                                        [
                                            "c"
                                        ],
                                        [
                                            "a",
                                            tag_link
                                        ]
                                    ]
                                ],
                                [
                                    f' {message}'
                                ]
                            ],
                            "created_by_table": "notion_user",
                            "created_by_id": "00000000-0000-0000-0000-000000000000",
                            "alive": True,
                            "id": new_comment_id,
                            "version": 1
                        }
                    },
                    {
                        "id": parent_id,
                        "table": "discussion",
                        "path": [
                            "comments"
                        ],
                        "command": "listAfter",
                        "args": {
                            "id": new_comment_id
                        }
                    },
                    {
                        "table": "comment",
                        "id": new_comment_id,
                        "path": [
                            "created_time"
                        ],
                        "command": "set",
                        "args": timestamp
                    },
                    {
                        "table": "comment",
                        "id": new_comment_id,
                        "path": [
                            "last_edited_time"
                        ],
                        "command": "set",
                        "args": timestamp
                    }
                ]
            }
        ]
    }
    self.post('saveTransactions', transaction)
