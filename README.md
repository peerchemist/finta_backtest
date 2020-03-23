![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# finta_backtest

Framework for backtesting trading strategies in Python, based on the [finta](https://github.com/peerchemist/finta) library.

## Why finta_backtest and not some other library?

I've decided to implement finta_backtest after trying out pretty much all of Python backtesting libraries I could find on github. Lockdown following COVID-19 pandemic probably had had some influence on my decisions as well.
I've wanted to test out some trading strategies implemented using indicators found in finta library, and that required some modifications on libraries I could found. This however made me look at overly complex codebase of various libraries, and I was not in mood of modifying more than than 50 lines of code.

Finta_backtest is made to be ultra small, fast and very easy to modify. The first release has less than 250 lines of code.

## Examples

See tests/test_unit.py.

## Roadmap

Right now library is pretty much proof-of-concept.
For the near future plan is to make it feature complete when compared to similar libs, after that focus will be on documentation and examples.

## Contributing

1. Fork it (https://github.com/peerchemist/finta_backtest/fork)
2. Study how it's implemented.
3. Create your feature branch (`git checkout -b my-new-feature`).
4. Run [black](https://github.com/ambv/black) code formatter on the finta.py to ensure uniform code style.
5. Commit your changes (`git commit -am 'Add some feature'`).
6. Push to the branch (`git push origin my-new-feature`).
7. Create a new Pull Request.
