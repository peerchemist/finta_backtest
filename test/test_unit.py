import os
import pytest
import pandas as pd
from finta import TA
from finta_backtest import Backtest, Strategy


@pytest.fixture
def rootdir():

    return os.path.dirname(os.path.abspath(__file__))


data_file = os.path.join(rootdir(), 'data/xau-usd.json')

# using tail 500 rows only
ohlc = pd.read_json(data_file, orient=["time"]).set_index("time").tail(50)


class TRIXCross(Strategy):

    """
    Trix cross
    """

    def __init__(
        self, ohlc: pd.DataFrame, period: int = 20,
    ) -> None:
        self.ohlc = ohlc
        self.period = period

    @property
    def name(self):
        return f"TrixCross ({self.period_slow})"

    def buy_signal(self):

        trix = TA.TRIX(self.ohlc, self.period)
        signal = trix > 0

        return signal

    def sell_signal(self):

        return -self.buy_signal()


trixcross = TRIXCross(ohlc, 2)
assert isinstance(trixcross, Strategy)

bt = Backtest(trixcross, deposit=1000, only_long=True)
assert isinstance(bt, Backtest)

report = bt.run()
assert isinstance(report, dict)

