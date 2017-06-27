"""
Manage cli to wrap ansible-galaxy command
"""

from invoke import Collection, Program
from ..tasks import ansible_galaxy as ansible_galaxy_tasks


def main(args=None):
    """
    Console script to manage aci-ansible-galaxy cli
    """

    program = Program(
        name='Ansible Customer Invoke taks to run "ansible-galaxy" commands',
        namespace=Collection.from_module(ansible_galaxy_tasks),
        version='0.1.0-alpha+001')

    program.run(args)
