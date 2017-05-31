"""
Ansible CLI testing
"""

import pytest
from ansible_customer.cli import ansible as ansible_cli


def test_cli_without_task(capsys):
    """
    Test cli usage without task
    """

    with pytest.raises(SystemExit) as exit_info:
        ansible_cli.main('aci-ansible')

    out, err = capsys.readouterr()

    assert exit_info.value.code == 0  # nosec
    assert err == ''  # nosec
    assert 'Usage:' in out  # nosec
    assert 'Subcommands:' in out  # nosec


def test_cli_run_task(capsys):
    """
    Test cli run task
    """

    ansible_cli.main('aci-ansible run')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage: ansible <host-pattern> [options]' in out  # nosec
