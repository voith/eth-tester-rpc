import pytest


@pytest.mark.xfail
def test_eth_gasprice(rpc_client):
    result = rpc_client('eth_gasPrice')
    assert result == "0x1"
