from uuid import uuid1

from notion.client import NotionClient
from notion.collection import CollectionRowBlock


def init(token: str) -> NotionClient:
    client = NotionClient(token_v2=token)
    client.comment = __comment__
    return client


def get_discussion_id(self: NotionClient, page_id: str) -> str:
    record_map = self.post(
        "loadPageChunk",
        {
            "chunkNumber": 0,
            "pageId": page_id,
            "limit": 50,
            "verticalColumns": False,
        },
    ).json()["recordMap"]

    if "discussion" in record_map:
        return list(record_map["discussion"].keys())[0]
    else:
        return ""


def __comment__(
    self,
    page_id: str,
    **kwargs,
):
    discussion_id = get_discussion_id(self, page_id=page_id)
    transaction = (
        not discussion_id
        and build_start_discussion_transaction(page_id=page_id, **kwargs)
        or build_add_comment_transaction(
            discussion_id=discussion_id,
            **kwargs,
        )
    )
    self.post("saveTransactions", transaction)


def build_add_comment_transaction(
    discussion_id: str,
    tag_body: str,
    tag_link: str,
    body: str,
    author: str,
    timestamp: int,
) -> dict:
    request_id = str(uuid1())
    comment_id = str(uuid1())
    transaction_id = str(uuid1())
    return {
        "requestId": request_id,
        "transactions": [
            {
                "id": transaction_id,
                "spaceId": "15c95d23-c4d5-436e-aa3a-1acbc7f7876c",
                "operations": [
                    {
                        "id": comment_id,
                        "table": "comment",
                        "path": [],
                        "command": "set",
                        "args": {
                            "parent_id": discussion_id,
                            "parent_table": "discussion",
                            "text": [
                                [tag_body, [["c"], ["a", tag_link]]],
                                [
                                    f" {body}",
                                    [
                                        ["b"],
                                    ],
                                ],
                                [
                                    f" - {author}",
                                ],
                            ],
                            "created_by_table": "notion_user",
                            "created_by_id": "00000000-0000-0000-0000-000000000000",
                            "alive": True,
                            "id": comment_id,
                            "version": 1,
                        },
                    },
                    {
                        "id": discussion_id,
                        "table": "discussion",
                        "path": ["comments"],
                        "command": "listAfter",
                        "args": {"id": comment_id},
                    },
                    {
                        "table": "comment",
                        "id": comment_id,
                        "path": ["created_time"],
                        "command": "set",
                        "args": timestamp,
                    },
                    {
                        "table": "comment",
                        "id": comment_id,
                        "path": ["last_edited_time"],
                        "command": "set",
                        "args": timestamp,
                    },
                ],
            }
        ],
    }


def build_start_discussion_transaction(
    page_id: str,
    tag_body: str,
    tag_link: str,
    body: str,
    author: str,
    timestamp: int,
) -> dict:
    request_id = str(uuid1())
    comment_id = str(uuid1())
    transaction_id = str(uuid1())
    discussion_id = str(uuid1())
    notion_user_id = "00000000-0000-0000-0000-000000000000"
    return {
        "requestId": request_id,
        "transactions": [
            {
                "id": transaction_id,
                "spaceId": "15c95d23-c4d5-436e-aa3a-1acbc7f7876c",
                "operations": [
                    {
                        "id": comment_id,
                        "table": "comment",
                        "path": [],
                        "command": "set",
                        "args": {
                            "parent_id": discussion_id,
                            "parent_table": "discussion",
                            "text": [
                                [tag_body, [["c"], ["a", tag_link]]],
                                [
                                    f" {body}",
                                    [
                                        ["b"],
                                    ],
                                ],
                                [
                                    f" - {author}",
                                ],
                            ],
                            "alive": True,
                            "id": comment_id,
                            "version": 1,
                        },
                    },
                    {
                        "id": discussion_id,
                        "table": "discussion",
                        "path": [],
                        "command": "set",
                        "args": {
                            "id": discussion_id,
                            "parent_id": page_id,
                            "parent_table": "block",
                            "resolved": False,
                            "comments": [comment_id],
                            "version": 1,
                        },
                    },
                    {
                        "table": "block",
                        "id": page_id,
                        "path": ["discussions"],
                        "command": "listAfter",
                        "args": {"id": discussion_id},
                    },
                    {
                        "table": "comment",
                        "id": comment_id,
                        "path": ["created_by_id"],
                        "command": "set",
                        "args": notion_user_id,
                    },
                    {
                        "table": "comment",
                        "id": comment_id,
                        "path": ["created_by_table"],
                        "command": "set",
                        "args": "notion_user",
                    },
                    {
                        "table": "comment",
                        "id": comment_id,
                        "path": ["created_time"],
                        "command": "set",
                        "args": timestamp,
                    },
                    {
                        "table": "comment",
                        "id": comment_id,
                        "path": ["last_edited_time"],
                        "command": "set",
                        "args": timestamp,
                    },
                    {
                        "table": "block",
                        "id": page_id,
                        "path": ["last_edited_time"],
                        "command": "set",
                        "args": timestamp,
                    },
                ],
            }
        ],
    }
