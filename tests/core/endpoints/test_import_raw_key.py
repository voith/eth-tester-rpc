from eth_account import (
    Account,
)


def test_import_raw_key(rpc_client):
    account = Account.create()
    result = rpc_client('personal_importRawKey', params=[account.privateKey.hex()])
    assert result == account.address
