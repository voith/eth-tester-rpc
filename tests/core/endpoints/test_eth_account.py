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
