import vegaapiclient as vac


def test_ListAccounts(corenode_coreapi):
    req = vac.vega.coreapi.v1.coreapi.ListAccountsRequest()
    accounts = corenode_coreapi.ListAccounts(req).accounts
    assert len(accounts) > 0
