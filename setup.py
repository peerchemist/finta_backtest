from setuptools import setup
from os import path

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Financial and Insurance Industry",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
]

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="finta_backtest",
    version="0.0.2",
    description="Backtest trading strategies, based on the finta library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["technical analysis", "backtesting", "ta", "pandas", "finance", "numpy", "analysis"],
    url="https://github.com/peerchemist/finta_backtest",
    author="Peerchemist",
    author_email="peerchemist@protonmail.ch",
    license="LGPLv3+",
    packages=["finta_backtest"],
    install_requires=["finta"],
)
