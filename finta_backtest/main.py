from pandas import DataFrame
from abc import ABCMeta, abstractmethod
from typing import List, Any
from finta import TA


class Strategy(metaclass=ABCMeta):
    def __init__(self, ohlc: DataFrame) -> None:
        self.ohlc = ohlc

    @property
    @abstractmethod
    def name(self):
        """strategy name"""
        self.name

    def resample(self, interval: str) -> DataFrame:
        """resample column by <interval>"""

        d = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }

        return self.ohlc.resample(interval).agg(d)
        return resample(ohlc, interval)
    @abstractmethod
    def signal(self) -> DataFrame:
        """What is the buy signal?"""
        pass

    def candle_close(self) -> DataFrame:
        return self.ohlc.close

    def candle_open(self) -> DataFrame:
        return self.ohlc.open

    def candle_high(self) -> DataFrame:
        return self.ohlc.high

    def candle_low(self) -> DataFrame:
        return self.ohlc.low

    def candle_volume(self) -> DataFrame:
        return self.ohlc.volume


class Backtest(TA):
    def __init__(
        self,
        strategy: Strategy,
        deposit: float = 10000,
        only_long: bool = True,
        # partial_stock=True,
        # commission: str = "0.01%"
    ):

        self.strategy: Strategy = strategy
        self.spread: float = 0  # factor in slippage
        self.initial_deposit: float = deposit
        self.only_long: bool = only_long  # do we short trade or not?
        # self.partial_stock: bool = partial_stock  # can you buy partial?
        # assert commission.endswith("%"), "Please express comission as percentage."
        # self.commission = commission
        #  list of simulated trades
        self.trades: List = []
        #  inventory
        self.stock: float = 0
        #  cash on hand
        self.balance: float = deposit
        #  internal ledger
        self.ledger = self.strategy.ohlc.reindex(
            columns=[
                "close",
                "high",
                "low",
                "open",
                "volume",
                "signal",
                "balance",
                "stock",
            ]
        )
        #  fill relevant cells
        self.ledger["signal"] = self.strategy.signal()
        self.ledger.at[self.ledger.index[0], "balance"] = self.balance

    def _hodl(self) -> float:
        """what if we just buy and hold to the end"""

        entry = self.initial_deposit / self.ledger["close"][0]
        close = entry * self.ledger["close"][-1]

        return close

    def _update_ledger(self, index):
        """keep the internal ledger updated"""

        self.ledger.loc[index, "balance"] = self.balance
        self.ledger.loc[index, "stock"] = self.stock

    def _trade(self, row):
        """do the deed"""

        #  if there were no trades yet, None
        try:
            last_trade = self.trades[-1]
        except IndexError:
            last_trade = None

        timestamp = row.name

        if last_trade:
            #  going long
            if last_trade["action"] != "long" and row["signal"]:
                self._long(row["close"], timestamp)
                self._update_ledger(row.name)

            # covering long (booking profit)
            if last_trade["action"] is "long" and not row["signal"]:
                self._cover_long(row["close"], timestamp, last_trade)
                self._update_ledger(row.name)

            # if shorts are allowed
            if not self.only_long:
                # going short
                if last_trade["action"] != "short" and not row["signal"]:
                    self._short(row["close"], timestamp)
                    self._update_ledger(row.name)

                # covering short (booking profit)
                if last_trade["action"] is "short" and row["signal"]:
                    self._cover_short(row["close"], timestamp, last_trade)
                    self._update_ledger(row.name)

        else:  # the very first trade
            if row.signal:
                self._long(row["close"], timestamp)
                self._update_ledger(row.name)
            else:
                pass

    def _commission_calc(self, number: float) -> float:
        """factor in trade commission"""

        return number * float(self.commission.replace("%", "")) * 100

    def _long(self, price: float, timestamp: Any) -> None:
        """long logic"""

        # print("going long")

        amount = self.balance / price
        self.stock = self.stock + amount
        self.balance = 0

        self.trades.append(
            {
                "timestamp": timestamp,
                "action": "long",
                "price": price,
                "amount": amount,
            }
        )

    def _cover_long(self, price: float, timestamp: Any, last_trade: dict) -> None:
        """cover long logic"""

        # print("taking profit")

        amount = last_trade["amount"]
        self.stock = self.stock - amount
        profit = amount * price
        self.balance += profit

        self.trades.append(
            {
                "timestamp": timestamp,
                "action": "cover_long",
                "price": price,
                "amount": amount,
            }
        )

    def _short(self, price: float, timestamp: Any) -> None:
        """short logic"""

        # print("going short")

        amount = self.balance / price
        self.stock -= self.stock + amount
        self.balance = 0

        self.trades.append(
            {
                "timestamp": timestamp,
                "action": "short",
                "price": price,
                "amount": amount,
            }
        )

    def _cover_short(self, price: float, timestamp: Any, last_trade: dict) -> None:
        """cover short logic"""

        # print("taking profit")

        amount = last_trade["amount"]
        self.stock = 0
        profit = amount * price
        self.balance += profit

        self.trades.append(
            {
                "timestamp": timestamp,
                "action": "cover_short",
                "price": price,
                "amount": amount,
            }
        )

    def _purge_positions(self) -> None:
        """if there is remaining stock, simulate liquidation"""

        if self.trades[-1]["action"] == "short" and abs(self.stock) > 0:
            last_price = self.ledger["close"][-1]
            timestamp = self.ledger.index[-1]

            self._cover_short(last_price, timestamp, self.trades[-1])

        if self.trades[-1]["action"] == "long" and abs(self.stock) > 0:
            last_price = self.ledger["close"][-1]
            timestamp = self.ledger.index[-1]

            self._cover_long(last_price, timestamp, self.trades[-1])

    def report(self) -> dict:
        """compile report"""

        return {
            "starting_balance": self.initial_deposit,
            "final_balance": self.balance,
            "stock": self.stock,
            "profit": self.balance - self.initial_deposit,
            "number_of_trades": len(self.trades),
            "buy_and_hold_profit": self._hodl() - self.initial_deposit,
        }

    def run(self) -> dict:
        """run the simulation"""

        self.ledger.apply(self._trade, raw=False, axis=1)

        # if there are remaining positons close them
        self._purge_positions()

        return self.report()
