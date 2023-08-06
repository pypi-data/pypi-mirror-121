from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class Hangup(AsteriskCommand):
    ActionID: str
    Channel: str
    peerName: str
    Action: str = "Hangup"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Channel": self.Channel,
            "peerName": self.peerName,
        }
