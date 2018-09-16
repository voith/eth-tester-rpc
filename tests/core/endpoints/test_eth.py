from eth_tester.constants import (
    UINT256_MAX,
    UINT256_MIN,
)
from eth_utils import (
    is_address,
)


def test_eth_account(rpc_client):
    accounts = rpc_client('eth_accounts')
    assert accounts
    assert all(
        is_address(account)
        for account
        in accounts
    )


def test_eth_getBlock(rpc_client):
    block = rpc_client(
        'eth_getBlockByNumber',
        params=['0x01']
    )
    assert isinstance(block, dict)


def test_eth_getBalance(rpc_client):
    accounts = rpc_client('eth_accounts')
    for account in accounts:
        balance = rpc_client('eth_getBalance', params=[account, 'latest'])
        assert balance >= UINT256_MIN
        assert balance <= UINT256_MAX
