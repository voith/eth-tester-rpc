from tests.utils import (
    hex_to_int,
)


def test_eth_blockNumber(rpc_client):
    result = rpc_client('eth_blockNumber')
    assert hex_to_int(result) == 0
