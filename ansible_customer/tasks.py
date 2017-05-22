"""
This module contains all Invoke tasks of this package
"""

from invoke import task


@task
def fake_task(context):
    """
    Fake task for initialize cli module
    """

    context.run('echo fake task')
