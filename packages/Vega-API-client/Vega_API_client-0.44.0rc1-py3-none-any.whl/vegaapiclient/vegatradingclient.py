from .generated.vega.api import trading_pb2_grpc as trading_grpc
from .grpcclient import GRPCClient


class VegaTradingClient(GRPCClient):
    """
    The Vega Trading Client talks to a back-end node.
    """

    def __init__(self, url: str, channel=None) -> None:
        super().__init__(url, channel=channel)
        self._trading = trading_grpc.TradingServiceStub(self.channel)

    def __getattr__(self, funcname):
        return getattr(self._trading, funcname)
