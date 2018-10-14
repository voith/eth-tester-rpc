def test_eth_getUncleCountByBlockHash(rpc_client):
    block_number = rpc_client('eth_blockNumber')
    block = rpc_client(
        'eth_getBlockByNumber',
        params=[block_number]
    )
    count = rpc_client(
        method="eth_getUncleCountByBlockHash",
        params=[block['hash']]
    )

    assert count == 0
