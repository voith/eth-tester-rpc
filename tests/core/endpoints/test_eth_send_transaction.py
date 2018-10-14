def test_eth_sendTransaction(rpc_client, accounts):
    result = rpc_client(
        method="eth_sendTransaction",
        params=[{
            "from": accounts[0],
            "to": accounts[1],
            "value": 1234,
            "data": "0x1234",
            "gas": 100000,
            "gasPrice": 4321,
        }],
    )

    assert len(result) == 66

    txn = rpc_client(
        method="eth_getTransactionByHash",
        params=[result],
    )
    assert txn['from'] == accounts[0]
    assert txn['to'] == accounts[1]
    assert txn['value'] == 1234
    assert txn['gas'] == 100000
    assert txn['gasPrice'] == 4321


def test_eth_sendTransaction_no_gas(rpc_client, accounts):
    result = rpc_client(
        method="eth_sendTransaction",
        params=[{
            "from": accounts[0],
            "to": accounts[1],
            "value": 1234,
            "data": "0x1234",
        }],
    )

    assert len(result) == 66

    txn = rpc_client(
        method="eth_getTransactionByHash",
        params=[result],
    )
    assert txn['from'] == accounts[0]
    assert txn['to'] == accounts[1]
    assert txn['value'] == 1234
    assert 'gas' in txn
    assert 'gasPrice' in txn


def test_eth_sendTransaction_with_hex_values(rpc_client, accounts):
    result = rpc_client(
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

    assert len(result) == 66

    txn = rpc_client(
        method="eth_getTransactionByHash",
        params=[result],
    )
    assert txn['from'] == accounts[0]
    assert txn['to'] == accounts[1]
    assert txn['value'] == 1234
    assert txn['gas'] == 100000
    assert txn['gasPrice'] == 4321
