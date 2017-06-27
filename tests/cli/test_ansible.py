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
    assert excinfo.value.code != 0  # nosec


def test_cli_ping_task_without_limit(capsys, aci_ansible_project):
    """
    Test cli ping task without limit argument
    """

    ansible_cli.main('aci-ansible ping foo*')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'foo | SUCCESS' in out.strip()  # nosec
    assert 'foobar | SUCCESS' in out.strip()  # nosec
    assert '"ping": "pong"' in out.strip()  # nosec


def test_cli_ping_task_with_limit(capsys, aci_ansible_project):
    """
    Test cli ping task with limit argument
    """

    ansible_cli.main('aci-ansible ping foo* --limit=foobar')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'foo | SUCCESS' not in out.strip()  # nosec
    assert 'foobar | SUCCESS' in out.strip()  # nosec
    assert '"ping": "pong"' in out.strip()  # nosec


def test_cli_setup_task_without_hosts(capsys):
    """
    Test cli setup task without host mandatory argument
    """

    with pytest.raises(SystemExit) as excinfo:
        ansible_cli.main('aci-ansible setup')

    out, err = capsys.readouterr()

    assert err.strip() == (  # nosec
        "'setup' did not receive all required positional arguments!")
    assert out == ''  # nosec
    assert excinfo.value.code != 0  # nosec


def test_cli_setup_task_without_limit(capsys, aci_ansible_project):
    """
    Test cli setup task without limit argument
    """

    ansible_cli.main('aci-ansible setup foo*')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'foo | SUCCESS' in out.strip()  # nosec
    assert 'foobar | SUCCESS' in out.strip()  # nosec
    assert '"ansible_hostname": "aci-ansible-target"' in out.strip()  # nosec
    assert '"ansible_distribution_version": "16.04"' in out.strip()  # nosec


def test_cli_setup_task_with_limit(capsys, aci_ansible_project):
    """
    Test cli setup task with limit argument
    """

    ansible_cli.main('aci-ansible setup foo* --limit=foobar')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'foo | SUCCESS' not in out.strip()  # nosec
    assert 'foobar | SUCCESS' in out.strip()  # nosec
    assert '"ansible_hostname": "aci-ansible-target"' in out.strip()  # nosec
    assert '"ansible_distribution_version": "16.04"' in out.strip()  # nosec
