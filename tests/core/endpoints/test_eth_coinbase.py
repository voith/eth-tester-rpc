
def test_eth_coinbase(accounts, rpc_client):
    result = rpc_client('eth_coinbase')
    assert result == accounts[0]
