from eth_tester.constants import (
    UINT256_MAX,
    UINT256_MIN,
)

from tests.utils import (
    hex_to_int,
)


def test_eth_getBalance(rpc_client):
    accounts = rpc_client('eth_accounts')
    for account in accounts:
        balance = rpc_client('eth_getBalance', params=[account, 'latest'])
        balance = hex_to_int(balance)
        assert balance >= UINT256_MIN
        assert balance <= UINT256_MAX


def test_eth_getBalance_hex_value(rpc_client):
    accounts = rpc_client('eth_accounts')
    for account in accounts:
        balance = rpc_client('eth_getBalance', params=[account, hex(rpc_client('eth_blockNumber'))])
        balance = hex_to_int(balance)
        assert balance >= UINT256_MIN
        assert balance <= UINT256_MAX
