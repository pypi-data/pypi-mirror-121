import json
from typing import Dict, List
from abc import ABC, abstractmethod
from dataclasses import field
from AsteriskCommandApi.commons.asterisk_action import Action


class AsteriskCommand(ABC):
    Action: str
    auxiliar_commands: List
    Variables: Dict = field(default_factory=dict)
    is_asterisk_command: bool = True

    @abstractmethod
    def as_dict(self) -> Dict:
        raise NotImplementedError("Method not implemented")

    def as_json_asterisk_command(self) -> str:
        return json.dumps(self.as_dict())

    def as_asterisk_command(self) -> Action:
        return Action(name=self.Action, keys=self.as_dict(), variables=self.Variables)
