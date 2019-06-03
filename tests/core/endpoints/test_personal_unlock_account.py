import pytest

from tests.utils import hex_to_int


def test_personal_unlockAccount(accounts, rpc_client, password_account, account_password):
    initial_balance = rpc_client('eth_getBalance', [accounts[1]])

    # confirm it didn't start unlocked
    with pytest.raises(AssertionError):
        rpc_client('eth_sendTransaction', [{
            'from': password_account,
            'to': accounts[2],
            'value': 1234,
        }])
    assert rpc_client('eth_getBalance', [accounts[1]]) == initial_balance

    assert not rpc_client('personal_unlockAccount', [password_account, 'not-correct-password'])

    # confirm it didn't get unlocked.
    with pytest.raises(AssertionError):
        rpc_client('eth_sendTransaction', [{
            'from': password_account,
            'to': accounts[2],
            'value': 1234,
        }])
    assert rpc_client('eth_getBalance', [accounts[1]]) == initial_balance

    assert rpc_client('personal_unlockAccount', [password_account, account_password])

    # confirm it's unlocked
    rpc_client('eth_sendTransaction', [{
        'from': password_account,
        'to': accounts[1],
        'value': 1234,
    }])
    after_balance = rpc_client('eth_getBalance', [accounts[1]])

    assert hex_to_int(after_balance) - hex_to_int(initial_balance) == 1234
