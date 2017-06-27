#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'invoke==0.18.0',
    'molecule==2.0.0.0rc9',
]

test_requirements = []

setup(
    name='ansible_customer',
    version='0.1.0-alpha+001',
    description="Python module to manage an Ansible project, linked to Infopen cookiecutter-ansible-customer template.",
    long_description=readme + '\n\n' + history,
    author="Alexandre Chaussier",
    author_email='a.chaussier@infopen.pro',
    url='https://github.com/infOpen/ansible_customer',
    packages=[
        'ansible_customer',
        'ansible_customer.cli',
        'ansible_customer.tasks',
    ],
    package_dir={'ansible_customer':
                 'ansible_customer'},
    entry_points={
        'console_scripts': [
            'aci-ansible=ansible_customer.cli.ansible:main',
            'aci-ansible-galaxy=ansible_customer.cli.ansible_galaxy:main',
            'aci-ansible-playbook=ansible_customer.cli.ansible_playbook:main',
            'aci-molecule=ansible_customer.cli.molecule:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ansible_customer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
