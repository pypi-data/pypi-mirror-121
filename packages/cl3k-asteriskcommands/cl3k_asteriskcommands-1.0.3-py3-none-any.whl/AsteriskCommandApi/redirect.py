from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class Redirect(AsteriskCommand):
    ActionID: str
    Channel: str
    Context: str
    Exten: str
    Priority: str
    peerName: str
    Action: str = "Redirect"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Channel": self.Channel,
            "Context": self.Context,
            "Exten": self.Exten,
            "Priority": self.Priority,
            "peerName": self.peerName,
        }
