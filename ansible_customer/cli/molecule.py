"""
Manage cli to wrap molecule command
"""

from invoke import Collection, Program
from ..tasks import molecule as molecule_tasks


def main(args=None):
    """
    Console script to manage aci-molecule cli
    """

    program = Program(
        name='Ansible Customer Invoke taks to run "molecule" commands',
        namespace=Collection.from_module(molecule_tasks),
        version='0.1.0-alpha+001')

    program.run(args)
