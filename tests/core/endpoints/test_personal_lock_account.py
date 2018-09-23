from eth_account import (
    Account,
)
from eth_utils import (
    encode_hex,
)
import pytest


@pytest.fixture()
def account_password():
    return "a-password"


@pytest.fixture()
def account_private_key():
    return Account().create().privateKey


@pytest.fixture()
def account_public_key(account_private_key):
    return Account().privateKeyToAccount(account_private_key).address


@pytest.fixture()
def password_account(
        rpc_client,
        accounts,
        account_password,
        account_private_key,
        account_public_key
):
    address = rpc_client(
        'personal_importRawKey',
        [encode_hex(account_private_key), account_password],
    )
    assert address == account_public_key

    initial_balance = 1000000000000000000000  # 1,000 ether

    rpc_client('eth_sendTransaction', [{
        'from': accounts[0],
        'to': address,
        'value': initial_balance,
    }])

    assert rpc_client('eth_getBalance', [address]) == initial_balance
    return address


def test_personal_lockAccount(accounts, rpc_client, password_account, account_password):
    assert rpc_client('personal_unlockAccount', [password_account, account_password])

    initial_balance = rpc_client('eth_getBalance', [accounts[1]])

    # confirm it's unlocked
    rpc_client('eth_sendTransaction', [{
        'from': password_account,
        'to': accounts[1],
        'value': 1234,
    }])
    after_balance = rpc_client('eth_getBalance', [accounts[1]])

    assert after_balance - initial_balance == 1234

    assert rpc_client('personal_lockAccount', [password_account])

    # sanity check
    before_balance = rpc_client('eth_getBalance', [accounts[2]])

    with pytest.raises(AssertionError):
        # confirm it's now locked
        rpc_client('eth_sendTransaction', [{
            'from': password_account,
            'to': accounts[2],
            'value': 1234,
        }])

    # sanity check
    assert rpc_client('eth_getBalance', [accounts[2]]) == before_balance
