from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class GetAgentStatus(AsteriskCommand):
    ActionID: str
    Interface: str
    Action: str = "GetAgentStatus"
    is_asterisk_command: bool = False

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Interface": self.Interface,
        }
