from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class SetVar(AsteriskCommand):
    ActionID: str
    Channel: str
    Variable: str
    Value: str
    Action: str = "SetVar"

    def as_dict(self) -> Dict:
        return {
            "Action": self.Action,
            "ActionID": self.ActionID,
            "Channel": self.Channel,
            "Variable": self.Variable,
            "Value": self.Value,
        }
