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

``$ TOXENV=py27-ansible23 tox``

You can enable Paramiko debug if you have an error on Docker fixture create
(ex: ``Exception: Timeout reached while waiting on service!``)

``$ PARAMIKO_DEBUG=1 TOXENV=py27-ansible23 tox``

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

Setup
~~~~~

    ``aci-ansible setup my_hosts [--limit=foo]``

Simple task to run setup module over an host list.

Ansible-playbook cli wrapper
++++++++++++++++++++++++++++

    Entry point: ``aci-ansible-playbook``

This is the wrapper over the ``ansible-playbook`` command.

List-tags
~~~~~~~~~

    ``aci-ansible-playbook list_tags my_playbook``

Simple task to list tags managed by a playbook.

List-tasks
~~~~~~~~~~

    ``aci-ansible-playbook list_tasks my_playbook``

Simple task to list tasks managed by a playbook.

Run
~~~

    ``aci-ansible-playbook run my_playbook [--limit=foo]``

Simple task to run a playbook.

Ansible-galaxy cli wrapper
++++++++++++++++++++++++++

    Entry point: ``aci-ansible-galaxy``

This is the wrapper over the ``ansible-galaxy`` command.

Install
~~~~~~~

    ``aci-ansible-galaxy install requirement_file [-f]``

Simple task to install roles managed by the requirement file.

List-roles
~~~~~~~~~~

    ``aci-ansible-galaxy list_roles [--role-name=my_role]``

Simple task to list role(s) installed.

Remove
~~~~~~

    ``aci-ansible-galaxy remove my_role1[,my_role2,...]``

Simple task to remove role(s).

Molecule cli wrapper
++++++++++++++++++++

    Entry point: ``aci-molecule``

This is the wrapper over the ``molecule`` command.

Create
~~~~~~

    ``aci-molecule create scenario_name [--driver=docker]``

Simple task to start test instances.

Converge
~~~~~~~~

    ``aci-molecule converge scenario_name``

Simple task to configure test instances.

Destroy
~~~~~~~

    ``aci-molecule destroy scenario_name [--driver=docker]``

Simple task to destroy test instances.

Destroy
~~~~~~~

    ``aci-molecule list scenario_name [--output=simple]``

Simple task to list test instances status.

Login
~~~~~

    ``aci-molecule login scenario_name host``

Simple task to login into test instance.

Test
~~~~

    ``aci-molecule test scenario_name [--driver=docker]``

Simple task to run tests against instances and destroy them.

Verify
~~~~~~

    ``aci-molecule verify scenario_name``

Simple task to run automated tests against instances.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`Infopen Ansible customer cookiecutter template`: https://github.com/infOpen/cookiecutter-ansible-customer
.. _Invoke: https://github.com/pyinvoke/invoke
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
