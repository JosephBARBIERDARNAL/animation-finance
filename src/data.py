import yfinance as yf
import pandas as pd
import numpy as np
from typing import Union, List
from scipy import interpolate


def load_yahoo_data(tickers: Union[str, List[str]]) -> pd.DataFrame:
    """
    Load closing price data for one or multiple tickers from Yahoo Finance.
    Returns the maximum available data for all tickers.

    Args:
    tickers (str or list of str): Single ticker or list of tickers to fetch data for.

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

    merged_df["Index"] = pd.Series(range(1, len(merged_df) + 1))
    return merged_df.sort_values("Date")


def convert_base(a, base=100):
    a_trans = a[:].copy()
    a_trans[0] = base
    for i in range(1, len(a)):
        a_trans[i] = base + ((a[i] - a[0]) * 100 / a[0])
    return a_trans


def interpolate_data(
    df: pd.DataFrame, method: str = "linear", factor: float = 2
) -> pd.DataFrame:
    """
    Interpolate data to add more smooth points.

    Args:
    df (pandas.DataFrame): Input DataFrame with 'Index', 'Date', and ticker columns.
    method (str): Interpolation method. Options: 'linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic'.
    factor (float): Factor to multiply the number of points by for interpolation.

    Returns:
    pandas.DataFrame: DataFrame with interpolated data.
    """
    x = df["Index"].values
    num_points = int(len(x) * factor)
    new_x = np.linspace(x.min(), x.max(), num_points)

    interpolated_df = pd.DataFrame({"Index": new_x})

    date_nums = pd.to_numeric(df["Date"])
    f_date = interpolate.interp1d(x, date_nums, kind="linear")
    interpolated_df["Date"] = pd.to_datetime(f_date(new_x).astype(int))

    for column in df.columns:
        if column not in ["Index", "Date"]:
            f = interpolate.interp1d(x, df[column].values, kind=method)
            interpolated_df[column] = f(new_x)

    return interpolated_df
