from highlight_text import fig_text, ax_text
from matplotlib.ticker import FuncFormatter
from matplotlib.font_manager import FontProperties
from pypalettes import get_hex
import streamlit as st
from datetime import timedelta
from pyfonts import load_font
import time
import textwrap
import math

from src.utils import format_date
from src.text import count_closed_and_enclosed, remove_unmatched_lt
from src.tickers import company_tickers

linecolors = get_hex("AirNomads") + get_hex("Alacena")


def custom_formatter(x, pos):
    if x >= 1e6:
        return f"{x*1e-6:.0f}M"
    elif x >= 1e3:
        return f"{x*1e-3:.0f}k"
    else:
        return f"{x:.0f}"


def update(
    frame,
    df,
    ax,
    fig,
    tickers,
    my_bar,
    title,
    description,
    elements_to_draw,
    theme,
    output_format,
    font_name,
):
    # Skip first frame
    if frame == 0:
        return ax

    # set font
    font = load_font(
        font_url="https://github.com/google/fonts/blob/main/ofl/amaranth/Amaranth-Regular.ttf?raw=true"
    )
    bold_font = load_font(
        font_url="https://github.com/google/fonts/blob/main/ofl/amaranth/Amaranth-Bold.ttf?raw=true"
    )

    # apply theme
    ax.set_facecolor(theme["background-color"])
    ax.tick_params(color=theme["text-color"], labelcolor=theme["text-color"])
    for spine in ax.spines.values():
        spine.set_edgecolor(theme["text-color"])

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
    subset_df = df.iloc[:frame]
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
            subset_df["Index"].values[-1] + 1,
            subset_df[ticker].values[-1],
            f"{company_tickers[ticker]} (${subset_df[ticker].values[-1]:,.0f})",
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
        subset_df[tickers].min(axis=1).min() * 0.95,
        subset_df[tickers].max(axis=1).max() * 1.05,
    )
    ax.set_xticks([])

    # get text position according to output format
    if output_format == "Portrait":
        x_pos = 0.1
        x_pos_credit = 0.6
        y_pos_credit = 0.05
        y_pos_title = 0.98
        y_pos_subtitle = 0.96
        y_pos_date = 0.94
        y_pos_description = 0.9
        max_text_wrap = 75
    elif output_format == "Landscape":
        x_pos = 0.07
        x_pos_credit = 0.8
        y_pos_credit = 0.05
        y_pos_title = 0.94
        y_pos_subtitle = 0.9
        y_pos_date = 0.86
        y_pos_description = 0.8
        max_text_wrap = 160
    elif output_format == "Square":
        x_pos = 0.12
        x_pos_credit = 0.6
        y_pos_credit = 0.05
        y_pos_title = 0.94
        y_pos_subtitle = 0.9
        y_pos_date = 0.86
        y_pos_description = 0.8
        max_text_wrap = 75

    # title
    fig_text(
        x=x_pos,
        y=y_pos_title,
        s=title,
        fontsize=25,
        ha="left",
        color=theme["text-color"],
        font=bold_font,
    )

    # subtitle
    first_date = format_date(df["Date"].min())
    last_date = format_date(subset_df["Date"].max()).upper()
    fig_text(
        x=x_pos,
        y=y_pos_subtitle,
        s=f"$100 invested in {first_date}",
        fontsize=20,
        ha="left",
        color=theme["text-color"],
        font=font,
    )
    fig_text(
        x=x_pos,
        y=y_pos_date,
        s=f"{last_date}",
        fontsize=16,
        color="grey",
        ha="left",
        font=font,
    )

    # credit
    fig_text(
        x=x_pos_credit,
        y=y_pos_credit,
        s=f"Developed by <barbierjoseph.com>",
        highlight_textprops=[{"font": bold_font}],
        font=font,
        fontsize=12,
        color=theme["text-color"],
    )

    # get text to display at current frame
    total_chars = len(description)
    effective_frame_count = len(df) - 50
    num_chars = (
        math.ceil(total_chars * (frame / effective_frame_count))
        if frame < effective_frame_count
        else total_chars
    )
    current_description = description[:num_chars]
    current_description = remove_unmatched_lt(
        current_description
    )  # remove unmatched '<' characters
    num_closed_tags = count_closed_and_enclosed(
        current_description
    )  # count number of closed tags
    if num_closed_tags > 0:
        highlight_textprops = [{"font": bold_font} for _ in range(num_closed_tags)]
    else:
        highlight_textprops = None
    wrapped_text = "\n".join(
        [
            textwrap.fill(paragraph, width=max_text_wrap)
            for paragraph in current_description.split("\n")
        ]
    )
    fig_text(
        x_pos,
        y_pos_description,
        wrapped_text,
        ha="left",
        va="top",
        fontsize=14,
        font=font,
        color=theme["text-color"],
        highlight_textprops=highlight_textprops,
        fig=fig,
    )

    fig.set_tight_layout(True)

    return ax


def make_animation(
    frame,
    df,
    ax,
    fig,
    tickers,
    my_bar,
    title,
    description,
    elements_to_draw,
    theme,
    output_format,
    font_name,
):
    result = update(
        frame,
        df,
        ax,
        fig,
        tickers,
        my_bar,
        title,
        description,
        elements_to_draw,
        theme,
        output_format,
        font_name,
    )
    return ax
