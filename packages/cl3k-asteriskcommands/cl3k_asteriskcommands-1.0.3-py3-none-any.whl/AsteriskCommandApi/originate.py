from typing import Dict
from dataclasses import dataclass, field
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class Originate(AsteriskCommand):
    ActionID: str
    Channel: str
    Context: str
    Exten: str
    Priority: str
    Callerid: str
    Timeout: str
    Variables: Dict = field(default_factory=dict)
    Action: str = "Originate"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Channel": self.Channel,
            "Context": self.Context,
            "Exten": self.Exten,
            "Priority": self.Priority,
            "Callerid": self.Callerid,
            "Timeout": self.Timeout,
            "Variables": self.Variables,
        }
