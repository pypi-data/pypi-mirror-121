from typing import Dict
from dataclasses import dataclass
from AsteriskCommand.commons.asterisk_command import AsteriskCommand


@dataclass
class QueueStatus(AsteriskCommand):
    ActionID: str
    Action: str = "QueueStatus"

    def as_dict(self) -> Dict:
        return {"Action": self.Action, "ActionID": self.ActionID}
