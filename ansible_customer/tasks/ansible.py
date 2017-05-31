"""
Invoke tasks to be used with ansible cli
"""

from invoke import task


@task
def run(context):
    """
    Ansible command call with all task arguments - NOT IMPLEMENTED - See #11

    """

    context.run('ansible --help')
