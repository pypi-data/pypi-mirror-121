from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class CoreShowChannels(AsteriskCommand):
    ActionID: str
    Action: str = "CoreShowChannels"

    def as_dict(self) -> Dict:
        return {"Action": self.Action, "ActionID": self.ActionID}
