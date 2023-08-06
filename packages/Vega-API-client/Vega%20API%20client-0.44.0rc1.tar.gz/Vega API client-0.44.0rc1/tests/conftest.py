import os

import pytest
import vegaapiclient as vac


@pytest.fixture(scope="module")
def corenode_trading():
    """
    Provide a `VegaTradingClient`, connected to `$CORE_GRPC_NODE`.
    """
    grpc_node = os.getenv("CORE_GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    return vac.VegaTradingClient(grpc_node)


@pytest.fixture(scope="module")
def corenode_coreapi():
    """
    Provide a `VegaCoreAPIClient`, connected to `$CORE_GRPC_NODE`.
    """
    grpc_node = os.getenv("CORE_GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    return vac.VegaCoreAPIClient(grpc_node)


@pytest.fixture(scope="module")
def datanode_tradingdata():
    """
    Provide a `TBD`, connected to `$DATA_GRPC_NODE`.
    """
    grpc_node = os.getenv("DATA_GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    raise Exception("Not implemented: datanode_tradingdata")
    # return vac.TBD(grpc_node)


@pytest.fixture(scope="module")
def datanode_tradingproxy():
    """
    Provide a `TBD`, connected to `$DATA_GRPC_NODE`.
    """
    grpc_node = os.getenv("DATA_GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    raise Exception("Not implemented: datanode_tradingproxy")
    # return vac.TBD(grpc_node)
