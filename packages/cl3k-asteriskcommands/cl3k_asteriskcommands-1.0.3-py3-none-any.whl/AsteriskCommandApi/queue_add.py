from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class QueueAdd(AsteriskCommand):
    ActionID: str
    Queue: str
    Interface: str
    Penalty: str
    Paused: str
    MemberName: str
    StateInterface: str
    Action: str = "QueueAdd"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Queue": self.Queue,
            "Interface": self.Interface,
            "Penalty": self.Penalty,
            "Paused": self.Paused,
            "MemberName": self.MemberName,
            "StateInterface": self.StateInterface,
        }
