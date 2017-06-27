"""
Manage cli to wrap ansible-playbook command
"""

from invoke import Collection, Program
from ..tasks import ansible_playbook as ansible_playbook_tasks


def main(args=None):
    """
    Console script to manage aci-ansible-playbook cli
    """

    program = Program(
        name='Ansible Customer Invoke taks to run "ansible-playbook" commands',
        namespace=Collection.from_module(ansible_playbook_tasks),
        version='0.1.0-alpha+001')

    program.run(args)
