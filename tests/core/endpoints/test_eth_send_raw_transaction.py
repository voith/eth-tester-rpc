from eth_account import (
    Account,
)
from eth_keys import (
    keys,
)
from eth_utils import (
    encode_hex,
    int_to_big_endian,
)


def int_to_private_key(i):
    pk_bytes = int_to_big_endian(i).rjust(32, b'\x00')
    return keys.PrivateKey(pk_bytes)


def test_eth_sendRawTransaction(accounts, rpc_client):
    p_key = int_to_private_key(1)
    assert p_key.public_key.to_checksum_address() == accounts[0]
    account = Account.privateKeyToAccount(p_key)
    tx = {
        "nonce": rpc_client(
            method="eth_getTransactionCount",
            params=[accounts[0]],
        ),
        "from": accounts[0],
        "to": accounts[1],
        "gas": 210000,
        "gasPrice": 1,
    }
    raw_tx = account.signTransaction(tx).rawTransaction

    result = rpc_client('eth_sendRawTransaction', params=[encode_hex(raw_tx)])
    assert len(result) == 66
