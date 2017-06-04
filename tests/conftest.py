import os
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException, \
    NoValidConnectionsError
import pytest
import requests


def _check_sshd_service(ip_address, ssh_port):
    """
    Ensure SSHd service running on the container
    """

    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        ssh_client.connect(ip_address, port=ssh_port)
    except AuthenticationException:
        return True
    except (SSHException, NoValidConnectionsError):
        return False


@pytest.fixture(scope='session')
def aci_ansible_target(docker_ip, docker_services):
    """
    Ensure that "some service" is up and responsive.
    """

    ssh_port = docker_services.port_for('aci-ansible-target', 22)

    # Check SSH connection before next steps
    docker_services.wait_until_responsive(
       timeout=30.0, pause=0.1,
       check=lambda: _check_sshd_service(docker_ip, ssh_port)
    )

    return {'ip': docker_ip, 'ssh_port': ssh_port}


@pytest.fixture(scope='session')
def aci_ansible_structure(tmpdir_factory, aci_ansible_target):
    """
    This fixture manage a basic ansible project structure with:
    * hosts file
    * private key file
    """

    BASE_IMAGE_PRIVATE_KEY_URL = (
        'https://github.com/phusion/baseimage-docker/raw/master/image/'
        + 'services/sshd/keys/insecure_key')

    hosts_infos = 'ansible_host={} ansible_user=root ansible_port={}'.format(
        aci_ansible_target.get('ip'),
        aci_ansible_target.get('ssh_port')
    )

    hosts_file_content = [
        'foo {}'.format(hosts_infos),
        'bar {}'.format(hosts_infos),
        'foobar {}'.format(hosts_infos),
    ]

    base_image_private_key = requests.get(BASE_IMAGE_PRIVATE_KEY_URL)

    base_dir = tmpdir_factory.mktemp('ansible_config')
    base_dir.join('hosts').write('\n'.join(hosts_file_content))
    base_dir.join('ssh_key').write(base_image_private_key.content)
    base_dir.join('ssh_key').chmod(0o400)

    return base_dir


@pytest.fixture(scope='session')
def aci_ansible_project(aci_ansible_structure):
    """
    Prepare environment vars to work with aci_ansible_project fixture
    """

    inventory_path = aci_ansible_structure.join('hosts').strpath
    private_key_path = aci_ansible_structure.join('ssh_key').strpath

    os.environ['ANSIBLE_INVENTORY'] = inventory_path
    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = str(False)
    os.environ['ANSIBLE_PRIVATE_KEY_FILE'] = private_key_path
