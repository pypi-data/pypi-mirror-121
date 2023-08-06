import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class Hangup(AsteriskCommand):
    ActionID: str
    Channel: str
    peerName: str
    Action: str = "Hangup"
