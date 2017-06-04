================
Ansible customer
================


.. image:: https://img.shields.io/pypi/v/ansible_customer.svg
        :target: https://pypi.python.org/pypi/ansible_customer

.. image:: https://img.shields.io/travis/infOpen/ansible_customer.svg
        :target: https://travis-ci.org/infOpen/ansible_customer

.. image:: https://readthedocs.org/projects/ansible-customer/badge/?version=latest
        :target: https://ansible-customer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/infOpen/ansible_customer/shield.svg
        :target: https://pyup.io/repos/github/infOpen/ansible_customer/
        :alt: Updates

.. image:: https://pyup.io/repos/github/infOpen/ansible_customer/python-3-shield.svg
        :target: https://pyup.io/repos/github/infOpen/ansible_customer/
        :alt: Python 3

.. image:: https://img.shields.io/codecov/c/github/infOpen/ansible_customer/master.svg?label=coverage_master
        :target: https://codecov.io/gh/infOpen/ansible_customer
        :alt: Codecov master

.. image:: https://img.shields.io/codecov/c/github/infOpen/ansible_customer/develop.svg?label=coverage_develop
        :target: https://codecov.io/gh/infOpen/ansible_customer
        :alt: Codecov develop

.. image:: https://img.shields.io/codacy/grade/10406cf9151649b7865a75704c95640d/master.svg?label=code_quality_master
        :target: https://www.codacy.com/app/achaussier/ansible_customer
        :alt: Codacy master

.. image:: https://img.shields.io/codacy/grade/10406cf9151649b7865a75704c95640d/develop.svg?label=code_quality_develop
        :target: https://www.codacy.com/app/achaussier/ansible_customer
        :alt: Codacy develop

-------------------------------------------------------------------------------

Python module to manage an Ansible project, linked to `Infopen Ansible customer cookiecutter template`_.

It expose some cli to manage an Ansible project, with settings for each environment.

We use Invoke_ tasks, linked to their cli to run commands inside contexts.


* Free software: MIT license
* Documentation: https://ansible-customer.readthedocs.io.


Testing
-------

    You must have **Docker >= 1.13.0** installed to run the tests. We use it to check Ansible
    commands

To run tests locally, just run needed environments using tox:
``$ TOXENV=py27-ansible20 tox``

Features
--------

Ansible cli wrapper
+++++++++++++++++++

    Entry point: ``aci-ansible``

This is the wrapper over the ``ansible`` command.

Ping
~~~~

    ``aci-ansible ping my_hosts [--limit=foo]``

Simple task to run ping module over an host list.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`Infopen Ansible customer cookiecutter template`: https://github.com/infOpen/cookiecutter-ansible-customer
.. _Invoke: https://github.com/pyinvoke/invoke
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
