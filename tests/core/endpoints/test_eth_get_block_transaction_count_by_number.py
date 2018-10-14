def test_eth_getBlockTransactionCountByNumber(rpc_client, accounts):
    block_number = rpc_client('eth_blockNumber')
    count = rpc_client(
        method="eth_getBlockTransactionCountByNumber",
        params=[block_number]
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
    count = rpc_client(
        method="eth_getBlockTransactionCountByNumber",
        params=[block_number]
    )

    assert count == 1
