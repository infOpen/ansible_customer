"""
Invoke tasks to be used with ansible cli
"""

from invoke import task
import os


def _run_basic_command(context, hosts, module, limit=''):
    """
    Ansible basic command template with only hosts, limit and module options
    """

    pty_enabled = not bool(os.environ.get('INVOKE_PTY'))

    context.run('ansible -m {module} --limit={limit} {hosts}'.format(
        limit=limit, hosts=hosts, module=module), pty=pty_enabled)


@task
def ping(context, hosts, limit=''):
    """
    Ansible command to run setup module on needed hosts
    """

    _run_basic_command(context, hosts, 'ping', limit)


@task
def run(context):
    """
    Ansible command call with all task arguments - NOT IMPLEMENTED - See #11
    """

    context.run('ansible --help')


@task
def setup(context, hosts, limit=''):
    """
    Ansible command to run setup module on needed hosts
    """

    _run_basic_command(context, hosts, 'setup', limit)
