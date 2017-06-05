"""
Ansible-galaxy CLI testing
"""

import pytest
from ansible_customer.cli import ansible_galaxy as ansible_galaxy_cli


def test_cli_without_task(capsys):
    """
    Test cli usage without task
    """

    with pytest.raises(SystemExit) as exit_info:
        ansible_galaxy_cli.main('aci-ansible-galaxy')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage:' in out  # nosec
    assert 'Subcommands:' in out  # nosec
    assert exit_info.value.code == 0  # nosec


def test_cli_direct_task(capsys):
    """
    Test cli direct task
    """

    with pytest.raises(SystemExit) as excinfo:
        ansible_galaxy_cli.main('aci-ansible-galaxy direct')

    out, err = capsys.readouterr()

    assert err != ''  # nosec
    assert 'Usage: ansible-galaxy' in out  # nosec
    assert excinfo.value.code != 0  # nosec


@pytest.mark.parametrize('name', [
    ('install'),
    ('remove'),
])
def test_cli_tasks_without_argument(capsys, name):
    """
    Test cli tasks without mandatory argument
    """

    with pytest.raises(SystemExit) as excinfo:
        ansible_galaxy_cli.main('aci-ansible-galaxy {}'.format(name))

    out, err = capsys.readouterr()

    assert err.strip() == (  # nosec
        "'{}' did not receive all required positional arguments!".format(name))
    assert out == ''  # nosec
    assert excinfo.value.code != 0  # nosec


@pytest.mark.parametrize('force,status', [
    (False, 'was installed successfully'),
    (False, 'is already installed'),
    (True, 'was installed successfully'),
])
def test_cli_install_task(capsys, aci_ansible_project, force, status):
    """
    Test cli install task
    """

    ansible_galaxy_cli.main('aci-ansible-galaxy install {} {}'.format(
        aci_ansible_project.join('requirements.yml').strpath,
        '-f' if force else '')
    )
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'infOpen.locales {}'.format(status) in out.strip()  # nosec
    assert 'infOpen.sysfs {}'.format(status) in out.strip()  # nosec


@pytest.mark.parametrize('role_name', [
    (''),
    ('infOpen.locales'),
])
def test_cli_list_task(capsys, aci_ansible_project, role_name):
    """
    Test cli list task
    """

    ansible_galaxy_cli.main(
        'aci-ansible-galaxy list --role-name={}'.format(role_name))
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'infOpen.locales' in out.strip()  # nosec
    if role_name == '':
        assert 'infOpen.sysfs' in out.strip()  # nosec
    else:
        assert 'infOpen.sysfs' not in out.strip()  # nosec


@pytest.mark.parametrize('role_name,status', [
    ('infOpen.locales', 'successfully removed {}'),
    ('infOpen.sysfs', 'successfully removed {}'),
    ('infOpen.locales', '{} is not installed, skipping'),
    ('infOpen.sysfs', '{} is not installed, skipping'),
])
def test_cli_remove_task(capsys, aci_ansible_project, role_name, status):
    """
    Test cli remove task
    """

    ansible_galaxy_cli.main('aci-ansible-galaxy remove {}'.format(role_name))
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert status.format(role_name) in out.strip()  # nosec
