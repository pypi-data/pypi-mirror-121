from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class Queues(AsteriskCommand):
    ActionID: str
    Action: str = "Queues"

    def as_dict(self) -> Dict:
        return {"Action": self.Action, "ActionID": self.ActionID}
