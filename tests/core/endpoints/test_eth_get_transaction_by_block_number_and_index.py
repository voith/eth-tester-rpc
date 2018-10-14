def test_eth_getTransactionByBlockNumberAndIndex_for_unknown_hash(rpc_client):
    result = rpc_client(
        method="eth_getTransactionByBlockNumberAndIndex",
        params=[999999999999999999999999999999999999999, 0],
    )

    assert result is None


def test_eth_getTransactionByBlockNumberAndIndex(rpc_client, accounts):
    tx_hash = rpc_client(
        method="eth_sendTransaction",
        params=[{
            "from": accounts[0],
            "to": accounts[1],
            "value": 1234,
            "data": "0x1234",
            "gas": 100000,
        }],
    )
    block_number = rpc_client('eth_blockNumber')
    txn = rpc_client(
        method="eth_getTransactionByBlockNumberAndIndex",
        params=[block_number, 0]
    )

    assert txn
    assert txn['hash'] == tx_hash
