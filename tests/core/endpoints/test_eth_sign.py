from tests.utils import (
    ecrecover,
)


def test_eth_sign(rpc_client):
    account = rpc_client('eth_accounts')[0]
    message = "0xdeadbeaf"
    signature = rpc_client('eth_sign', params=[account, message])
    assert ecrecover(signature, message) == account
