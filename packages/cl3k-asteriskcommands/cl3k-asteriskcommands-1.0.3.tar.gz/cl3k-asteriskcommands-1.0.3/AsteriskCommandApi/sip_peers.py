from typing import Dict
from dataclasses import dataclass
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@dataclass
class SIPpeers(AsteriskCommand):
    ActionID: str
    Action: str = "SIPpeers"

    def as_dict(self) -> Dict:
        return {"Action": self.Action, "ActionID": self.ActionID}
