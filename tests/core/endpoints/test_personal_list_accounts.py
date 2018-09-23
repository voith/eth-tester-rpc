
def test_personal_listAccounts(accounts, rpc_client):
    actual = rpc_client('personal_listAccounts')
    n_actual = set(actual)
    n_expected = set(accounts)

    assert n_actual == n_expected
