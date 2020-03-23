from finta import TA
from finta_backtest import Strategy


class EMACross(Strategy):

    """
    Naive EMA period/period_slow EMA cross.
    """

    def __init__(self, ohlc, period: int = 15, period_slow: int = 25) -> None:
        self.ohlc = ohlc
        self.period = period
        self.period_slow = period_slow

    @property
    def name(self):
        return f"EMACross ({self.period, self.period_slow})"

    def signal(self):

        ma_fast = TA.EMA(self.ohlc, self.period)
        ma_slow = TA.EMA(self.ohlc, self.period_slow)
        signal = ma_fast > ma_slow

        return signal
