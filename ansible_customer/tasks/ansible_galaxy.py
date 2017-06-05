"""
Invoke tasks to be used with ansible-galaxy cli
"""

from invoke import task
import os


def _run_basic_command(context, action='', options=None):
    """
    Ansible-galaxy basic command template with only action and optional options
    """

    pty_enabled = not bool(os.environ.get('INVOKE_PTY'))
    options = options or []

    context.run('ansible-galaxy {action} {options}'.format(
        action=action,
        options=' '.join(options)),
        pty=pty_enabled
    )


@task
def direct(context):
    """
    Ansible-galaxy command call with all task arguments - NOT IMPLEMENTED
    - See #11
    """

    context.run('ansible-galaxy --help')


@task
def install(context, requirements_file, force=False):
    """
    Ansible-galaxy command to install roles
    """

    command_options = ['-r {}'.format(requirements_file)]

    if force:
        command_options.append('-f')

    _run_basic_command(context, 'install', options=command_options)


@task
def list_roles(context, role_name=''):
    """
    Ansible-galaxy command to list roles
    """

    command_options = [role_name]
    _run_basic_command(context, 'list', options=command_options)


@task
def remove(context, role_names):
    """
    Ansible-galaxy command to remove roles
    """

    command_options = role_names.split(',')
    _run_basic_command(context, 'remove', options=command_options)
