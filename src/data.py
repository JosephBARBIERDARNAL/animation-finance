import yfinance as yf
import pandas as pd
from typing import Union, List
import streamlit as st


def load_yahoo_data(tickers: Union[str, List[str]], base: bool = False) -> pd.DataFrame:
    """
    Load closing price data for one or multiple tickers from Yahoo Finance.
    Returns the maximum available data for all tickers.

    Args:
    tickers (str or list of str): Single ticker or list of tickers to fetch data for.
    base (bool): If True, convert prices to base 100. Default is False.

    Returns:
    pandas.DataFrame: DataFrame containing the closing prices for all tickers.
    """
    if isinstance(tickers, str):
        tickers = [tickers]

    data_frames = []
    for ticker in tickers:
        df = yf.Ticker(ticker).history(period="max")
        df = df.reset_index()[["Date", "Close"]]
        df = df.rename(columns={"Close": ticker})
        data_frames.append(df)

    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = pd.merge(merged_df, df, on="Date", how="inner")

    if base:
        for ticker in tickers:
            merged_df[ticker] = convert_base(merged_df[ticker])

    return merged_df.sort_values("Date")


def convert_base(a, b=100):
    a_trans = a[:].copy()
    a_trans[0] = b
    for i in range(1, len(a)):
        a_trans[i] = b + ((a[i] - a[0]) * 100 / a[0])
    return a_trans
