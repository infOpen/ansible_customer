"""
Invoke tasks to be used with molecule cli
"""

from invoke import task, exceptions
import os


def _run_basic_command(context, action, scenario, options=None):
    """
    Molecule basic command template
    """

    pty_enabled = not bool(os.environ.get('INVOKE_PTY'))
    options = options or []

    context.run(
        'molecule {action} --scenario-name={scenario} {options}'.format(
            action=action,
            scenario=scenario,
            options=''.join(options)),
        pty=pty_enabled
    )


@task
def create(context, scenario, driver_name='docker'):
    """
    Molecule command to start instances
    """

    command_options = ['--driver-name={}'.format(driver_name)]
    _run_basic_command(context, 'create', scenario, options=command_options)


@task
def run(context):
    """
    Molecule command call with all task arguments - NOT IMPLEMENTED - See #11
    """

    pty_enabled = not bool(os.environ.get('INVOKE_PTY'))
    context.run('molecule --help', pty=pty_enabled)


@task
def converge(context, scenario):
    """
    Molecule command using a provisioner to configure instances
    """

    _run_basic_command(context, 'converge', scenario)


@task
def destroy(context, scenario, driver_name='docker'):
    """
    Molecule command to destroy instances
    """

    command_options = ['--driver-name={}'.format(driver_name)]
    _run_basic_command(context, 'destroy', scenario, options=command_options)


@task
def list(context, scenario, output='simple'):
    """
    Molecule command to list status of instances
    """

    if output not in ['simple', 'plain', 'yaml']:
        raise exceptions.ParseError('Incorrect output value')

    command_options = ['--format={}'.format(output)]

    _run_basic_command(context, 'list', scenario, options=command_options)


@task
def login(context, scenario, host):
    """
    Molecule command to login into instance
    """

    command_options = ['--host={}'.format(host)]
    _run_basic_command(context, 'login', scenario, options=command_options)


@task
def test(context, scenario, driver_name='docker'):
    """
    Molecule command to run tests against instances and destroy them
    """

    command_options = ['--driver-name={}'.format(driver_name)]
    _run_basic_command(context, 'test', scenario, options=command_options)


@task
def verify(context, scenario):
    """
    Molecule command to run automated tests against instances
    """

    _run_basic_command(context, 'verify', scenario)
