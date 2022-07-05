from tests.validations import python_validations, shell_validations, javascript_validations, cmd_failing_validations, cmd_passing_validations
from iamscan.policy import Policy
import subprocess
import pytest


class TestCommandLine:

    @pytest.mark.parametrize("command", cmd_failing_validations)
    def test_failing_commands(self, command):
        with pytest.raises(Exception) as e:
            
            subprocess.check_output("python -m " + command, shell=True)

    
    @pytest.mark.parametrize("command", cmd_passing_validations)
    def test_passing_commands(self, command):

        subprocess.check_output("python -m " + command, shell=True)



class TestActions:

    @pytest.mark.parametrize("source_file, expected_actions", javascript_validations)
    def test_javascript_parser(self, source_file, expected_actions):

        policy = Policy()

        policy.json['Statement'] = []

        policy.update_policy(f"tests/js/{source_file}")

        actions = policy.json['Statement'][0]['Action']

        assert (actions) == expected_actions

    @pytest.mark.parametrize("source_file, expected_actions", python_validations)
    def test_python_parser(self, source_file, expected_actions):

        policy = Policy()

        policy.json['Statement'] = []

        policy.update_policy(f"tests/py/{source_file}")

        actions = policy.json['Statement'][0]['Action']

        assert (actions) == expected_actions

    
    @pytest.mark.parametrize("source_file, expected_actions", shell_validations)
    def test_shell_parser(self, source_file, expected_actions):

        policy = Policy()

        policy.json['Statement'] = []

        policy.update_policy(f"tests/sh/{source_file}")

        actions = policy.json['Statement'][0]['Action']

        assert (actions) == expected_actions




