import errno
import logging
import os

from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException, \
    NoValidConnectionsError
import pytest
import requests
import shutil


def _create_or_update_symplink(target, link_name):
    """
    Create or update a symlink
    """

    try:
        os.symlink(target, link_name)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise error


def _check_sshd_service(ip_address, ssh_port):
    """
    Ensure SSHd service running on the container
    """

    with SSHClient() as ssh_client:

        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        # Add Paramiko transport console logger if requested
        if os.environ.get('PARAMIKO_DEBUG'):
            paramiko_logger = logging.getLogger('paramiko.transport')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(asctime)s | %(levelname)-8s| PARAMIKO: '
                                  '%(lineno)03d@%(module)-10s| %(message)s')
            )
            paramiko_logger.addHandler(console_handler)
            paramiko_logger.setLevel(logging.DEBUG)

        # Check with bad credentials to raise an AuthenticationException
        try:
            ssh_client.connect(  # nosec
                ip_address,
                port=ssh_port,
                username='root',
                password='foobar',
                allow_agent=False,
                look_for_keys=False)
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
    base_dir.join('roles').mkdir()
    base_dir.join('hosts').write('\n'.join(hosts_file_content))
    base_dir.join('ssh_key').write(base_image_private_key.content)
    base_dir.join('ssh_key').chmod(0o400)
    shutil.copy2(
        os.path.join(os.getcwd(), 'tests/resources/ansible/basic_play.yml'),
        base_dir.join('basic_play.yml').strpath
    )
    shutil.copy2(
        os.path.join(os.getcwd(), 'tests/resources/ansible/requirements.yml'),
        base_dir.join('requirements.yml').strpath
    )

    return base_dir


@pytest.fixture(scope='session')
def aci_ansible_project(aci_ansible_structure):
    """
    Prepare environment vars to work with aci_ansible_project fixture
    """

    inventory_path = aci_ansible_structure.join('hosts').strpath
    private_key_path = aci_ansible_structure.join('ssh_key').strpath
    roles_path = aci_ansible_structure.join('roles').strpath

    os.environ['ANSIBLE_INVENTORY'] = inventory_path
    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = str(False)
    os.environ['ANSIBLE_PRIVATE_KEY_FILE'] = private_key_path
    os.environ['ANSIBLE_ROLES_PATH'] = roles_path

    return aci_ansible_structure


@pytest.fixture(scope='session')
def aci_molecule_project(tmpdir_factory):
    """
    This fixture manage a basic molecule scenario structure with:
    * create and destroy playbooks
    * molecule configuration file
    * playbook to run
    """

    base_dir = tmpdir_factory.mktemp('molecule_config')
    base_dir.join('molecule').mkdir()

    scenario_dir = base_dir.join('molecule').join('basic-scenario')
    scenario_dir.mkdir()
    scenario_dir.join('tests').mkdir()

    managed_filenames = [
        'Dockerfile',
        'create.yml',
        'destroy.yml',
        'molecule.yml',
        'playbook.yml',
        'requirements.yml',
        '.yamllint',
    ]

    for filename in managed_filenames:
        shutil.copy2(
            os.path.join(
                os.getcwd(),
                'tests/resources/molecule/{}'.format(filename)),
            scenario_dir.join('{}'.format(filename)).strpath
        )

    shutil.copy2(
        os.path.join(
            os.getcwd(), 'tests/resources/molecule/tests/test_default.py'),
        scenario_dir.join('tests').join('test_default.py').strpath
    )

    _create_or_update_symplink(base_dir.join('molecule').strpath, 'molecule')
