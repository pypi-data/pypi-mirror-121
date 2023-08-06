from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.redirect import Redirect
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_redirect(self):
        action_id = str(uuid4())

        asterisk_command = Redirect(
            ActionID=action_id,
            Context="redirect",
            Exten="123",
            Priority="1",
            Channel="SIP/999",
            peerName="SIP/888",
        )

        expected_dictionary = {
            "Action": "Redirect",
            "ActionID": action_id,
            "Context": "redirect",
            "Exten": "123",
            "Priority": "1",
            "Channel": "SIP/999",
            "peerName": "SIP/888",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: Redirect
                ActionID: {action_id}
                Channel: SIP/999
                Context: redirect
                Exten: 123
                Priority: 1
                peerName: SIP/888
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
