import pytest


@pytest.fixture(scope='session')
def ansible_project(tmpdir_factory):
    """
    This fixture manage a basic ansible project structure with:
    * hosts file
    """

    HOSTS_CONTENT = [
        'foo ansible_host=127.0.0.1',
        'bar ansible_host=127.0.0.1',
        'foobar ansible_host=127.0.0.1',
    ]

    base_dir = tmpdir_factory.mktemp('ansible_config')
    base_dir.join('hosts').write('\n'.join(HOSTS_CONTENT))

    return base_dir
