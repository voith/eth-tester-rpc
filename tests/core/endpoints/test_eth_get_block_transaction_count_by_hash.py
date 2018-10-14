
def test_eth_getBlockTransactionCountByHash(rpc_client, accounts):
    block_number = rpc_client('eth_blockNumber')
    block = rpc_client(
        'eth_getBlockByNumber',
        params=[block_number]
    )
    count = rpc_client(
        method="eth_getBlockTransactionCountByHash",
        params=[block['hash']]
    )
    assert count == 0

    rpc_client(
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
    count = rpc_client(
        method="eth_getBlockTransactionCountByHash",
        params=[block['hash']]
    )

    assert count == 1
