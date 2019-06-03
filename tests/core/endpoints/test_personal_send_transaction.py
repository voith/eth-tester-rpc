import pytest

from tests.utils import hex_to_int


def test_personal_sendTransaction(accounts, rpc_client, password_account, account_password):
    initial_balance = rpc_client('eth_getBalance', [accounts[1]])

    # confirm it fails with a bad password
    with pytest.raises(AssertionError):
        rpc_client('personal_sendTransaction', [{
            'from': password_account,
            'to': accounts[1],
            'value': 1234,
            'gas': 21000,
        }, "incorrect-password"])
    assert rpc_client('eth_getBalance', [accounts[1]]) == initial_balance

    rpc_client('personal_sendTransaction', [{
        'from': password_account,
        'to': accounts[1],
        'value': 1234,
        'gas': 21000,
    }, account_password])
    after_balance = rpc_client('eth_getBalance', [accounts[1]])

    assert hex_to_int(after_balance) - hex_to_int(initial_balance) == 1234
