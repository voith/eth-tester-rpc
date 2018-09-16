from eth_tester.constants import (
    UINT256_MAX,
    UINT256_MIN,
)
from eth_utils import (
    is_address,
    is_checksum_address,
)
import pytest

# def test_eth_protocolVersion(w3):
#     with pytest.raises(ValueError):
#         w3.eth.protocolVersion
#
#
# def test_eth_syncing(w3):
#     with pytest.raises(ValueError):
#         w3.eth.syncing
#
#
# def test_eth_coinbase(w3):
#     coinbase = w3.eth.coinbase
#     assert is_checksum_address(coinbase)


def test_eth_account(rpc_client):
    accounts = rpc_client('eth_accounts')
    assert accounts
    assert all(
        is_address(account)
        for account
        in accounts
    )


# def test_eth_getBalance(w3):
#     accounts = w3.eth.accounts
#     for account in accounts:
#         balance = w3.eth.getBalance(account)
#         assert balance >= UINT256_MIN
#         assert balance <= UINT256_MAX
