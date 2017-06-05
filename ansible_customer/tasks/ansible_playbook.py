"""
Invoke tasks to be used with ansible-playbook cli
"""

from invoke import task
import os


def _run_basic_command(context, playbook, limit='', options=None):
    """
    Ansible-playbook basic command template with only hosts, limit and module
    options
    """

    pty_enabled = not bool(os.environ.get('INVOKE_PTY'))
    options = options or []

    context.run('ansible-playbook {playbook} --limit={limit} {options}'.format(
        limit=limit,
        options=' '.join(options),
        playbook=playbook),
        pty=pty_enabled
    )


@task
def direct(context):
    """
    Ansible-playbook command call with all task arguments - NOT IMPLEMENTED
    - See #11
    """

    context.run('ansible-playbook --help')


@task
def list_tags(context, playbook):
    """
    Ansible command to list playbook tags
    """

    command_options = ['--list-tags']
    _run_basic_command(context, playbook, options=command_options)


@task
def list_tasks(context, playbook):
    """
    Ansible command to list playbook tasks
    """

    command_options = ['--list-tasks']
    _run_basic_command(context, playbook, options=command_options)


@task
def run(context, playbook, limit=''):
    """
    Ansible-playbook command to run playbook
    """

    command_options = []
    _run_basic_command(context, playbook, limit, options=command_options)
