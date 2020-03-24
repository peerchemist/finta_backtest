## How to write a strategy

Strategy is defined as a `class`, which inherits `Strategy` metaclass.
For this reason, you need to import `Strategy` first.

> from finta_backtest import Strategy

Strategy class has a couple of mandatory methods and properties:

* ``__init__``
* ``name``
* ``signal``

Trying to initialize strategy class without those will result in error.

### def init

`__init__` requires `ohlc` DataFrame containing open,high,low,close candle data as minimum.
The rest of parameters are optional and depend on the indicator you plan to use. These are mostly `period`, ie. number of lookback candles for the indicator.

### def name

Name of the strategy, do as you like.

### signal

The most important method, this is where magic happens.
`signal` method must return pandas Series with index matching the `ohlc` and boolean (True/False) values.

For example, a simple cross of two EMA's.

```
    ma_fast = TA.EMA(self.ohlc, self.period)
    ma_slow = TA.EMA(self.ohlc, self.period_slow)
```

That defines two EMA's, in pandas it's easy to find out where do they cross each other.

`signal = ma_fast > ma_slow`

This will result in `True` when `ma_fast` is greater than `ma_slow`.

```
class EMACross(Strategy):

    """
    Naive EMA period/period_slow EMA cross.
    """

    def __init__(self, ohlc, period: int = 15, period_slow: int = 25) -> None:
        self.ohlc = ohlc
        self.period = period
        self.period_slow = period_slow

    @property
    def name(self) -> str:
        return f"EMACross ({self.period, self.period_slow})"

    def signal(self) -> pd.Series:

        ma_fast = TA.EMA(self.ohlc, self.period)
        ma_slow = TA.EMA(self.ohlc, self.period_slow)
        signal = ma_fast > ma_slow

        return signal
```