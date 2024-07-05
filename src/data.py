import yfinance as yf
import polars as pl
from typing import Union, List


def load_yahoo_data(tickers: Union[str, List[str]]) -> pl.DataFrame:
    """
    Load closing price data for one or multiple tickers from Yahoo Finance.
    Returns the maximum available data for all tickers.

    Args:
    tickers (str or list of str): Single ticker or list of tickers to fetch data for.

    Returns:
    polars.DataFrame: DataFrame containing the closing prices for all tickers.
    """
    if isinstance(tickers, str):
        tickers = [tickers]

    data_frames = []
    for ticker in tickers:
        df = yf.Ticker(ticker).history(period="max")
        df = pl.from_pandas(df.reset_index())
        df = df.select([pl.col("Date"), pl.col("Close").alias(ticker)])
        data_frames.append(df)

    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = merged_df.join(df, on="Date", how="inner")

    return merged_df.sort("Date")
