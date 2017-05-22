# -*- coding: utf-8 -*-

"""
This module manage the cli for this package
"""


from invoke import Collection, Program
from . import tasks


def main(args=None):
    """Console script for ansible_customer"""

    program = Program(
        name='Ansible Customer Invoke tasks',
        namespace=Collection.from_module(tasks),
        version='0.1.0')
    program.run(args)


if __name__ == "__main__":
    main()
