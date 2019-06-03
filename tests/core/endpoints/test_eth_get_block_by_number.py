
def test_eth_getBlock(rpc_client):
    block = rpc_client(
        'eth_getBlockByNumber',
        params=['0x01']
    )
    assert isinstance(block, dict)


def test_eth_getBlock_full_tx(rpc_client, accounts):
    rpc_client(
        method="eth_sendTransaction",
        params=[{
            "from": accounts[0],
            "to": accounts[1],
            "value": hex(1234),
            "data": "0x1234",
            "gas": hex(100000),
            "gasPrice": hex(4321),
        }],
    )
    block_number = rpc_client('eth_blockNumber')
    block = rpc_client(
        'eth_getBlockByNumber',
        params=[block_number, True]
    )
    assert len(block['transactions']) == 1
    assert 'gasPrice' in block['transactions'][0]
    assert isinstance(block, dict)
