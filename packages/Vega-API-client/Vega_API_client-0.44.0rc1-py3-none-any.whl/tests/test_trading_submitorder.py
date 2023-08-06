import vegaapiclient as vac


def test_order_submission(
    corenode_trading,
    corenode_coreapi,
):
    # Get the chain time
    timereq = vac.vega.api.trading.GetVegaTimeRequest()
    now = int(corenode_trading.GetVegaTime(timereq).timestamp)

    # Create the tx
    vac.vega.wallet.v1.wallet.SubmitTransactionRequest(
        pub_key="aabbcc",
        propagate=False,
        order_submission=vac.vega.commands.v1.commands.OrderSubmission(
            market_id="1234",
            price="10",
            size=1,
            side=vac.vega.vega.Side.SIDE_BUY,
            time_in_force=vac.vega.vega.Order.TimeInForce.TIME_IN_FORCE_GTT,
            expires_at=now + 120000000000,
            type=vac.vega.vega.Order.Type.TYPE_LIMIT,
            reference="sdk-python:test_order_submission",
            # pegged_order=None,
        ),
    )
