from eth_account import (
    Account,
)

from tests.utils import (
    ecrecover,
)


def test_eth_sign(rpc_client):
    account = rpc_client('eth_accounts')[0]
    message = "0xdeadbeaf"
    signature = rpc_client('eth_sign', params=[account, message])
    assert ecrecover(signature, message) == account


def test_eth_sign_new_private_key(rpc_client):
    account = Account.create()
    result = rpc_client('personal_importRawKey', params=[account.privateKey.hex()])
    assert result == account.address
    message = "0xdeadbeaf"
    signature = rpc_client('eth_sign', params=[account.address, message])
    assert ecrecover(signature, message) == account.address
