from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class SIPpeerstatus(AsteriskCommand):
    ActionID: str
    Action: str = "SIPpeerstatus"

    def as_dict(self) -> Dict:
        return {"Action": self.Action, "ActionID": self.ActionID}
