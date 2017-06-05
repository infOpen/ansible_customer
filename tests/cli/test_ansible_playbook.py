"""
Ansible-playbook CLI testing
"""

import pytest
import re
from ansible_customer.cli import ansible_playbook as ansible_playbook_cli


def test_cli_without_task(capsys):
    """
    Test cli usage without task
    """

    with pytest.raises(SystemExit) as exit_info:
        ansible_playbook_cli.main('aci-ansible-playbook')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage:' in out  # nosec
    assert 'Subcommands:' in out  # nosec
    assert exit_info.value.code == 0  # nosec


def test_cli_direct_task(capsys):
    """
    Test cli direct task
    """

    ansible_playbook_cli.main('aci-ansible-playbook direct')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage: ansible-playbook playbook.yml' in out  # nosec


@pytest.mark.parametrize('name', [
    ('list_tags'),
    ('list_tasks'),
    ('run'),
])
def test_cli_tasks_without_playbook(capsys, name):
    """
    Test cli tasks without playbook mandatory argument
    """

    with pytest.raises(SystemExit) as excinfo:
        ansible_playbook_cli.main('aci-ansible-playbook {}'.format(name))

    out, err = capsys.readouterr()

    assert err.strip() == (  # nosec
        "'{}' did not receive all required positional arguments!".format(name))
    assert out == ''  # nosec
    assert excinfo.value.code != 0  # nosec


def test_cli_list_tags_task_with_playbook(capsys, aci_ansible_project):
    """
    Test cli list_tags task
    """

    ansible_playbook_cli.main('aci-ansible-playbook list_tags {}'.format(
        aci_ansible_project.join('basic_play.yml').strpath)
    )
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'play #1 (all): Basic playbook' in out.strip()  # nosec
    assert 'TAGS: [playbook::basic-playbook]' in out.strip()  # nosec
    assert (  # nosec
        'TASK TAGS: [playbook::basic-playbook, '
        'playbook::basic-playbook::sshd, '
        'playbook::basic-playbook::sshd::keys, '
        'playbook::basic-playbook::sshd::service]') in out.strip()


def test_cli_list_tasks_task_with_playbook(capsys, aci_ansible_project):
    """
    Test cli list_tasks task
    """

    ansible_playbook_cli.main('aci-ansible-playbook list_tasks {}'.format(
        aci_ansible_project.join('basic_play.yml').strpath)
    )
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'play #1 (all): Basic playbook' in out.strip()  # nosec
    assert 'TAGS: [playbook::basic-playbook]' in out.strip()  # nosec
    assert 'Ensure openssh-server service running' in out.strip()  # nosec
    assert (  # nosec
        'TAGS: [playbook::basic-playbook, playbook::basic-playbook::sshd, '
        'playbook::basic-playbook::sshd::service]') in out.strip()
    assert 'Ensure root authorized_keys file exists' in out.strip()  # nosec
    assert (  # nosec
        'TAGS: [playbook::basic-playbook, playbook::basic-playbook::sshd, '
        'playbook::basic-playbook::sshd::keys]') in out.strip()


def test_cli_run_task_without_limit(capsys, aci_ansible_project):
    """
    Test cli run task
    """

    ansible_playbook_cli.main('aci-ansible-playbook run {}'.format(
        aci_ansible_project.join('basic_play.yml').strpath)
    )
    out, err = capsys.readouterr()

    test_regex = r'.*{}\s*:\s*ok=3\s*changed=0\s*unreachable=0\s*failed=0.*'

    assert err == ''  # nosec
    for hostname in ['foo', 'bar', 'foobar']:
        assert re.search(test_regex.format(hostname), out) is not None  # nosec


def test_cli_run_task_with_limit(capsys, aci_ansible_project):
    """
    Test cli run task
    """

    ansible_playbook_cli.main('aci-ansible-playbook run {} --limit=bar'.format(
        aci_ansible_project.join('basic_play.yml').strpath)
    )
    out, err = capsys.readouterr()

    test_regex = r'.*\s+{}\s*:\s*ok=3\s*changed=0\s*unreachable=0\s*failed=0.*'

    assert err == ''  # nosec
    for hostname in ['foo', 'foobar']:
        assert re.search(test_regex.format(hostname), out) is None  # nosec
    assert re.search(test_regex.format('bar'), out) is not None  # nosec
