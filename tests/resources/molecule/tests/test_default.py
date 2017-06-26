import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    """
    Test hosts file properties
    """

    hosts_file = host.file('/etc/hosts')

    assert hosts_file.exists
    assert hosts_file.user == 'root'
    assert hosts_file.group == 'root'
