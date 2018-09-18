def test_eth_getBlock(rpc_client):
    block = rpc_client(
        'eth_getBlockByNumber',
        params=['0x01']
    )
    assert isinstance(block, dict)
