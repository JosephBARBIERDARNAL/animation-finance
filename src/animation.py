from highlight_text import fig_text, ax_text
from matplotlib.ticker import FuncFormatter
from matplotlib.font_manager import FontProperties
from pypalettes import get_hex
import streamlit as st
import time
from datetime import timedelta

from src.utils import format_date
from src.tickers import company_tickers

# set up the font properties
personal_path = "/Users/josephbarbier/Library/Fonts/"
font = FontProperties(fname=personal_path + "FiraSans-Light.ttf")
bold_font = FontProperties(fname=personal_path + "FiraSans-Medium.ttf")

linecolors = get_hex("Acadia") + get_hex("AirNomads") + get_hex("Alacena")


def custom_formatter(x, pos):
    if x >= 1e6:
        return f"{x*1e-6:.0f}M"
    elif x >= 1e3:
        return f"{x*1e-3:.0f}k"
    else:
        return f"{x:.0f}"


def update(frame, df, ax, fig, tickers, my_bar, title, elements_to_draw, theme):
    # Skip first frame
    if frame == 0:
        return ax

    # apply theme
    ax.set_facecolor(theme["background-color"])
    ax.tick_params(color=theme["title-color"], labelcolor=theme["title-color"])
    for spine in ax.spines.values():
        spine.set_edgecolor(theme["title-color"])

    # Calculate progress
    current_progress_value = (frame + 1) / len(df)

    # Update progress text
    progress_text = f"Work in progress ({current_progress_value*100:.1f}%)"
    if (frame + 1) == len(df):
        progress_text = f"Done"
    my_bar.progress(current_progress_value, text=progress_text)

    # initialize subset of data
    range_days = 30
    if frame < range_days:
        subset_df = df.iloc[:frame]
    else:
        subset_df = df.iloc[frame - range_days : frame]
    ax.clear()

    for i, ticker in enumerate(tickers):

        # create the chart
        if "line" in elements_to_draw:
            ax.plot(
                subset_df["Index"],
                subset_df[ticker],
                color=linecolors[i],
                linewidth=1.4,
            )
        if "final point" in elements_to_draw:
            ax.scatter(
                subset_df["Index"].values[-1],
                subset_df[ticker].values[-1],
                color=linecolors[i],
                s=100,
            )
        if "area" in elements_to_draw:
            ax.fill_between(
                subset_df["Index"],
                100,
                subset_df[ticker],
                color=linecolors[i],
                alpha=0.3,
            )

        # annotate the last point
        ax_text(
            subset_df["Index"].values[-1] + 2,
            subset_df[ticker].values[-1],
            f"{company_tickers[ticker]} ({subset_df[ticker].values[-1]:,.0f})",
            color=linecolors[i],
            fontsize=18,
            ha="left",
            va="center",
            font=bold_font,
            ax=ax,
        )

    # custom axes style
    ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))
    ax.set_ylim(
        subset_df[tickers].min(axis=1).min() * 0.9,
        subset_df[tickers].max(axis=1).max() * 1.1,
    )
    ax.set_xticks([])

    # title
    fig_text(
        x=0.15,
        y=0.98,
        s=title,
        fontsize=20,
        ha="left",
        color=theme["title-color"],
        font=bold_font,
    )

    # subtitle
    first_date = format_date(subset_df["Date"].min()).upper()
    last_date = format_date(subset_df["Date"].max()).upper()
    fig_text(
        x=0.15,
        y=0.94,
        s=f"{first_date}",
        fontsize=14,
        color="grey",
        ha="left",
        font=font,
    )

    fig.set_tight_layout(True)

    return ax
