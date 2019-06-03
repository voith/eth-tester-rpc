import os

import pytest
from selenium.webdriver.chrome.options import (
    Options,
)
from splinter import (
    Browser,
)

from tests.utils import (
    hex_to_int,
)

from .utils import (
    MetamaskExtension,
    change_maifest_key,
    download_metamask,
)

DRIVER_NAME = 'chrome'
METAMASK_VERSION = '6.5.3'
MANIFEST_KEY = "metamaskmetamaskmetamaskmetamask"
METAMASK_SEED_PHRASE = "around purse armed present " \
                       "black diamond dice abstract diary gold predict truth"
METAMASK_ADDRESS = "0x6Ef7E2dBc9b41C5081c8990c0327DcB8528bA05b"


@pytest.fixture()
def metamask_version():
    return METAMASK_VERSION


@pytest.fixture()
def manifest_key():
    return MANIFEST_KEY


@pytest.fixture()
def extension_basename(metamask_version):
    return f'metamask-chrome-{metamask_version}'


@pytest.fixture()
def extension_dir(extension_basename):
    var_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'var',
        )
    )
    return os.path.join(var_dir, extension_basename)


@pytest.fixture()
def manifest_path(extension_dir):
    return os.path.join(extension_dir, 'manifest.json')


@pytest.fixture()
def metamask_extension_path(
        metamask_version,
        extension_basename,
        extension_dir,
        manifest_path,
        manifest_key
):
    if not os.path.exists(extension_dir):
        os.makedirs(extension_dir)

    if not os.path.exists(manifest_path):
        download_metamask(metamask_version, extension_basename, extension_dir)

    assert os.path.exists(manifest_path)
    change_maifest_key(manifest_path, manifest_key)
    return extension_dir


@pytest.fixture()
def splinter_kwargs(metamask_extension_path):
    """Webdriver kwargs."""
    options = Options()
    options.add_argument(f'--load-extension={metamask_extension_path}')
    return dict(options=options)


@pytest.fixture()
def browser(splinter_kwargs):
    return Browser(DRIVER_NAME, **splinter_kwargs)


@pytest.fixture()
def initial_metamask_balance():
    return 10 ** 18 - 10 ** 17


@pytest.fixture()
def init_metamask_account(rpc_client, initial_metamask_balance):
    from_account = rpc_client('eth_accounts')[0]

    rpc_client(
        method="eth_sendTransaction",
        params=[{
            "from": from_account,
            "to": METAMASK_ADDRESS,
            "value": initial_metamask_balance,
        }],
    )
    balance = rpc_client(
        'eth_getBalance',
        params=['0x6Ef7E2dBc9b41C5081c8990c0327DcB8528bA05b', 'latest']
    )
    assert hex_to_int(balance) == initial_metamask_balance


@pytest.fixture()
def metamask(browser, open_port, init_metamask_account):
    _metamask = MetamaskExtension(
        browser,
        open_port,
        METAMASK_SEED_PHRASE,
        METAMASK_ADDRESS
    )
    _metamask.initialize()
    _metamask.change_network("testrpc")
    return _metamask
