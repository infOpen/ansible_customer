"""
Molecule CLI testing
"""

import pytest
import re
from ansible_customer.cli import molecule as molecule_cli
from ansible_customer.tasks import molecule as molecule_tasks


def test_cli_without_task(capsys):
    """
    Test cli usage without task
    """

    with pytest.raises(SystemExit) as exit_info:
        molecule_cli.main('aci-molecule')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage:' in out  # nosec
    assert 'Subcommands:' in out  # nosec
    assert exit_info.value.code == 0  # nosec


def test_cli_run_task(capsys):
    """
    Test cli run task
    """

    molecule_cli.main('aci-molecule run')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert 'Usage: molecule [OPTIONS] COMMAND [ARGS]' in out  # nosec


@pytest.mark.parametrize('action', [
    'create',
    'converge',
    'dependency',
    'destroy',
    'list',
    'login',
    'test',
    'verify',
])
def test_cli_tasks_without_scenario(capsys, action):
    """
    Test cli tasks without scenario mandatory argument
    """

    with pytest.raises(SystemExit) as excinfo:
        molecule_cli.main('aci-molecule {action}'.format(action=action))

    out, err = capsys.readouterr()

    error_msg = "'{action}' did not receive all required positional arguments!"
    assert re.search(error_msg.format(action=action), err.strip())  # nosec
    assert out == ''  # nosec
    assert excinfo.value.code != 0  # nosec


def test_cli_create_task(capsys, aci_molecule_project):
    """
    Test cli create task
    """

    molecule_cli.main('aci-molecule create basic-scenario')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert '--> Scenario: [basic-scenario]' in out.strip()  # nosec
    assert 'TASK [Build an Ansible compatible image]' in out.strip()  # nosec
    assert 'TASK [Create molecule instance(s)]' in out.strip()  # nosec
    assert 'failed=0' in out.strip()  # nosec


def test_cli_dependency_task(capsys, aci_molecule_project):
    """
    Test cli dependency task
    """

    molecule_cli.main('aci-molecule dependency basic-scenario')

    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert '--> Scenario: [basic-scenario]' in out.strip()  # nosec
    assert '--> Dependency: [galaxy]' in out.strip()  # nosec
    assert 'infOpen.locales' in out.strip()  # nosec
    assert 'Dependency completed successfully' in out.strip()  # nosec


def test_cli_converge_task(capsys, aci_molecule_project):
    """
    Test cli converge task
    """

    molecule_cli.main('aci-molecule converge basic-scenario')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert '--> Scenario: [basic-scenario]' in out.strip()  # nosec
    assert 'failed=0' in out.strip()  # nosec
    assert 'ok=14' in out.strip()  # nosec


def test_cli_list_task(capsys, aci_molecule_project):
    """
    Test cli list task
    """

    molecule_cli.main('aci-molecule list basic-scenario')
    out, err = capsys.readouterr()

    assert err.strip() == ''  # nosec
    regex = (
        'test-molecule-basic-scenario\s*'
        'Docker\s*Ansible\s*basic-scenario\s*True\s*True')
    assert re.search(regex, out.strip())  # nosec


def test_cli_list_task_with_bad_output(capsys):
    """
    Test cli list task
    """

    with pytest.raises(SystemExit) as exit_info:
        molecule_cli.main('aci-molecule list basic-scenario --output=foo')

    out, err = capsys.readouterr()

    assert 'Incorrect output value' in err.strip()  # nosec
    assert out.strip() == ''  # nosec
    assert exit_info.value.code != 0  # nosec


def test_cli_verify_task(capsys, aci_molecule_project):
    """
    Test cli verify task
    """

    molecule_cli.main('aci-molecule verify basic-scenario')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert re.search('test_hosts_file.*PASSED', out.strip())  # nosec
    assert 'Verifier completed successfully' in out.strip()  # nosec


def test_cli_login_task(mocker, capsys, aci_molecule_project):
    """
    Test cli login task

    This test check only internal call with propers arguments, because I not
    able to do a real functional test due to stty errors
    """

    mocker.patch(
        'ansible_customer.tasks.molecule._run_basic_command',
        return_value='Molecule login execute called')

    molecule_cli.main(
        'aci-molecule login basic-scenario test-molecule-basic-scenario')
    out, err = capsys.readouterr()

    molecule_tasks._run_basic_command.assert_called_with(
        mocker.ANY,
        'login',
        'basic-scenario',
        options=['--host=test-molecule-basic-scenario'])
    assert err == ''  # nosec
    assert out == ''  # nosec


def test_cli_destroy_task(capsys, aci_molecule_project):
    """
    Test cli destroy task
    """

    molecule_cli.main('aci-molecule destroy basic-scenario')
    out, err = capsys.readouterr()

    regex = 'ok=1\s*changed=1\s*unreachable=0\s*failed=0'
    assert err == ''  # nosec
    assert '--> Playbook: [destroy.yml]' in out.strip()  # nosec
    assert re.search(regex, out.strip())  # nosec


def test_cli_test_task(capsys, aci_molecule_project):
    """
    Test cli test task
    """

    molecule_cli.main('aci-molecule test basic-scenario')
    out, err = capsys.readouterr()

    assert err == ''  # nosec
    assert '--> Scenario: [basic-scenario]' in out.strip()  # nosec
    assert 'Dependency completed successfully' in out.strip()  # nosec
    assert 'Idempotence completed successfully' in out.strip()  # nosec
    assert 'Lint completed successfully' in out.strip()  # nosec
    assert 'Verifier completed successfully' in out.strip()  # nosec
