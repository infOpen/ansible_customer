"""
Manage cli to wrap ansible command
"""

from invoke import Collection, Program
from ..tasks import ansible as ansible_tasks


def main(args=None):
    """
    Console script to manage aci-ansible cli
    """

    program = Program(
        name='Ansible Customer Invoke taks to run "ansible" commands',
        namespace=Collection.from_module(ansible_tasks),
        version='0.1.0-alpha+001')

    program.run(args)
