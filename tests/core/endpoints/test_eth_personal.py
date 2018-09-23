from eth_account import Account
from eth_utils import encode_hex


def test_personal_importRawKey(rpc_client):
    account_manager = Account()
    private_key = account_manager.create().privateKey
    new_account = rpc_client('personal_importRawKey', [encode_hex(private_key), 'a-password'])
    assert rpc_client('personal_unlockAccount', [new_account, 'a-password']) is True
