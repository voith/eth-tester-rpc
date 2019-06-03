from decimal import (
    Decimal,
)
import time

from web3 import Web3

from tests.utils import (
    hex_to_int,
)


def test_metamask_get_balance(metamask, initial_metamask_balance):
    assert metamask.get_balance() == Decimal(str(initial_metamask_balance / 10 ** 18))


def test_metamask_get_deposit(metamask, initial_metamask_balance, rpc_client):
    initial_metamask_balance = Web3.fromWei(initial_metamask_balance, 'ether')
    account = rpc_client('eth_accounts')[0]
    account_inital_balance = rpc_client('eth_getBalance', params=[account, 'latest'])
    amount = initial_metamask_balance / 10
    metamask.deposit_amount(account, amount)
    time.sleep(3)
    new_metamsk_balance = metamask.get_balance()
    assert new_metamsk_balance < initial_metamask_balance
    new_account_balance = rpc_client('eth_getBalance', params=[account, 'latest'])
    assert hex_to_int(
        account_inital_balance
    ) + Web3.toWei(amount, 'ether') == hex_to_int(new_account_balance)
