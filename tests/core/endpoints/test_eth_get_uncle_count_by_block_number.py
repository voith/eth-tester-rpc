def test_eth_getUncleCountByBlockNumber(rpc_client):
    block_number = rpc_client('eth_blockNumber')
    count = rpc_client(
        method="eth_getUncleCountByBlockNumber",
        params=[block_number]
    )

    assert count == 0
