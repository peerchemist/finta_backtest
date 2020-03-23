import pandas as pd
from finta import TA
from finta_backtest import Strategy


class VolEMA(Strategy):

    """
    Simple volume based strategy, shows accumulation.
    If current candle has closed with volume greater then volume EMA, return True.
    """

    def __init__(self, ohlc: pd.DataFrame, periods: int = 11) -> None:
        self.ohlc = ohlc
        self.periods = periods

    @property
    def name(self):
        return f"volema{self.periods}"

    def signal(self):

        vol = pd.Series(TA.EMA(self.ohlc, self.periods, column="volume"), name="vol")

        signal = vol > vol.shift()

        return signal
