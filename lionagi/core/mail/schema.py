from collections import deque
from enum import Enum

from lionagi.core.schema.base_node import BaseRelatableNode


class MailCategory(str, Enum):
    MESSAGES = "messages"
    TOOL = "tool"
    SERVICE = "service"
    MODEL = "model"
    NODE = "node"
    CONTEXT = "context"
    NODE_ID = "node_id"
    START = "start"
    END = "end"


class BaseMail:

    def __init__(self, sender_id, recipient_id, category, package):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        try:
            if isinstance(category, str):
                category = MailCategory(category)
            if isinstance(category, MailCategory):
                self.category = category
            else:
                raise ValueError(
                    f"Invalid request title. Valid titles are" f" {list(MailCategory)}"
                )
        except Exception as e:
            raise ValueError(
                f"Invalid request title. Valid titles are "
                f"{list(MailCategory)}, Error: {e}"
            )
        self.package = package


class StartMail(BaseRelatableNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pending_outs = deque()

    def trigger(self, context, structure_id, executable_id):
        start_mail_content = {"context": context, "structure_id": structure_id}
        start_mail = BaseMail(
            sender_id=self.id_,
            recipient_id=executable_id,
            category="start",
            package=start_mail_content,
        )
        self.pending_outs.append(start_mail)
