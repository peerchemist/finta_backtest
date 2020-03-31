from finta import TA
from finta_backtest import Strategy


class CloseUnderDEMA(Strategy):

    """
    Candle closing under DEMA.
    """

    def __init__(self, ohlc, period: int = 10) -> None:
        self.ohlc = ohlc
        self.period = period

    @property
    def name(self):
        return f"CloseUnderDEMA({self.period})"

    def buy_signal(self):

        dema = TA.DEMA(self.ohlc, 20)

        return self.ohlc["close"] > dema

    def sell_signal(self):

        return -self.buy_signal()
