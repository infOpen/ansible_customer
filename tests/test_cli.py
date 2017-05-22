#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cli
----------------------------------

Tests for `ansible_customer.cli` module.
"""

import subprocess
import pytest

from ansible_customer import cli


def test_cli_from_import(capsys):
    """
    Test cli usage from import
    """

    with pytest.raises(SystemExit) as exit_info:
        cli.main('aci')

    out, err = capsys.readouterr()

    assert exit_info.value.code == 0
    assert err == ''
    assert 'Usage:' in out
    assert 'Subcommands:' in out


def test_cli_from_shell():
    """
    Test cli usage from shell
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./ansible_customer '
               '/usr/bin/env python '
               './ansible_customer/cli.py')

    command_output = subprocess.check_output(
        command, shell=True, stderr=subprocess.STDOUT)
    assert 'Usage:' in command_output.decode('utf-8')
    assert 'Subcommands:' in command_output.decode('utf-8')


def test_cli_with_bad_task_name(capsys):
    """
    Test cli usage from import
    """

    with pytest.raises(SystemExit) as exit_info:
        cli.main('aci bad_task_name')

    out, err = capsys.readouterr()

    assert exit_info.value.code == 1
    assert "No idea what 'bad_task_name' is!" in err
    assert out == ''


def test_cli_tasks_available(capsys):
    """
    Test cli tasks available
    """

    expected_tasks = {'fake_task   Fake task for initialize cli module'}

    with pytest.raises(SystemExit) as exit_info:
        cli.main('aci --list')

    out, err = capsys.readouterr()
    out_set = set(it.strip() for it in out.split("\n"))

    assert exit_info.value.code == 0
    assert err == ''
    assert expected_tasks.issubset(out_set)
