from finta import TA
from finta_backtest import Strategy


class EvMacd(Strategy):

    """
    Elastic Volume MACD cross strategy.
    """

    def __init__(
        self, ohlc, period: int = 20, period_slow: int = 30, signal_period: int = 9,
    ) -> None:
        self.ohlc = ohlc
        self.period = period
        self.slow_period = period_slow
        self.signal_period = signal_period

    @property
    def name(self):
        return f"EVMACD({self.period, self.slow_period})"

    def buy_signal(self):

        macd = TA.EV_MACD(self.ohlc, self.period, self.slow_period, self.signal_period)
        return macd["MACD"] > macd["SIGNAL"]

    def sell_signal(self):

        return -self.buy_signal()
