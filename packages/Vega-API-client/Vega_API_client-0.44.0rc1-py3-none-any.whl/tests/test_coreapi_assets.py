import vegaapiclient as vac


def test_ListAssets(corenode_coreapi):
    req = vac.vega.coreapi.v1.coreapi.ListAssetsRequest()
    assets = corenode_coreapi.ListAssets(req).assets
    assert len(assets) > 0
    asset_id = assets[0].id

    req = vac.vega.coreapi.v1.coreapi.ListAssetsRequest(asset=asset_id)
    assets = corenode_coreapi.ListAssets(req).assets
    assert len(assets) == 1
    assert assets[0].id == asset_id
