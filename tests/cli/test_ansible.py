"""
Ansible CLI testing
"""

import os
import pytest
from ansible_customer.cli import ansible as ansible_cli


def test_cli_without_task(capsys):
    """
    Test cli usage without task
    """

    with pytest.raises(SystemExit) as exit_info:
        ansible_cli.main('aci-ansible')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage:' in out  # nosec
    assert 'Subcommands:' in out  # nosec
    assert exit_info.value.code == 0  # nosec


def test_cli_run_task(capsys):
    """
    Test cli run task
    """

    ansible_cli.main('aci-ansible run')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage: ansible <host-pattern> [options]' in out  # nosec


def test_cli_ping_task_without_hosts(capsys):
    """
    Test cli ping task without host mandatory argument
    """

    with pytest.raises(SystemExit) as excinfo:
        ansible_cli.main('aci-ansible ping')

    out, err = capsys.readouterr()

    assert err.strip() == (  # nosec
        "'ping' did not receive all required positional arguments!")
    assert out == ''  # nosec
    assert excinfo.value.code == 1  # nosec


def test_cli_ping_task(capsys, ansible_project):
    """
    Test cli ping task
    """

    os.environ['ANSIBLE_INVENTORY'] = ansible_project.join('hosts').strpath
    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = False

    with pytest.raises(SystemExit) as excinfo:
        ansible_cli.main('aci-ansible ping foo*')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'foo | UNREACHABLE!' in out.strip()  # nosec
    assert 'foobar | UNREACHABLE!' in out.strip()  # nosec
    assert excinfo.value.code == 3  # nosec


def test_cli_ping_task_with_limit(capsys, ansible_project):
    """
    Test cli ping task with limit argument
    """

    os.environ['ANSIBLE_INVENTORY'] = ansible_project.join('hosts').strpath
    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = False

    with pytest.raises(SystemExit) as excinfo:
        ansible_cli.main('aci-ansible ping foo* --limit=foobar')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'foo | UNREACHABLE!' not in out.strip()  # nosec
    assert 'foobar | UNREACHABLE!' in out.strip()  # nosec
    assert excinfo.value.code == 3  # nosec
