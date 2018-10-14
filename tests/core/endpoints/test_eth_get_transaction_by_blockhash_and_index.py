def test_eth_getTransactionByBlockHashAndIndex_for_unknown_hash(rpc_client):
    result = rpc_client(
        method="eth_getTransactionByBlockHashAndIndex",
        params=["0x0000000000000000000000000000000000000000000000000000000000000000", 0],
    )

    assert result is None


def test_eth_getTransactionByBlockHashAndIndex(rpc_client, accounts):
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
    block = rpc_client(
        'eth_getBlockByNumber',
        params=[block_number]
    )
    txn = rpc_client(
        method="eth_getTransactionByBlockHashAndIndex",
        params=[block['hash'], 0]
    )

    assert txn
    assert txn['hash'] == tx_hash
