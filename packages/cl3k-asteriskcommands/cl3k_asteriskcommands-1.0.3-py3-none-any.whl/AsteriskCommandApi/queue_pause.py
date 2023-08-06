from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class QueuePause(AsteriskCommand):
    ActionID: str
    Queue: str
    Interface: str
    Paused: str
    Reason: str
    MemberName: str
    Action: str = "QueuePause"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Queue": self.Queue,
            "Interface": self.Interface,
            "Paused": self.Paused,
            "Reason": self.Reason,
            "MemberName": self.MemberName,
        }
