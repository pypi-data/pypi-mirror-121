from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class QueueRemove(AsteriskCommand):
    ActionID: str
    Queue: str
    Interface: str
    Action: str = "QueueRemove"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Queue": self.Queue,
            "Interface": self.Interface,
        }
