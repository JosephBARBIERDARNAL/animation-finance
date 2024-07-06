from highlight_text import fig_text, ax_text
from matplotlib.ticker import FuncFormatter


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
    ticker,
    my_bar,
    line_color,
    title,
    elements_to_draw,
    linewidth,
    point_size,
):

    # skip first frame
    if frame == 0:
        return None

    # make the progress bar progress
    current_progress_value = (frame + 1) / len(df)
    progress_text = f"Work in progress ({current_progress_value*100:.1f}%)"
    my_bar.progress(current_progress_value, text=progress_text)

    # initialize subset of data
    subset_df = df.iloc[:frame]
    ax.clear()

    # create the chart
    if "line" in elements_to_draw:
        ax.plot(
            subset_df["Date"], subset_df[ticker], color=line_color, linewidth=linewidth
        )
    if "final point" in elements_to_draw:
        ax.scatter(
            subset_df["Date"].values[-1],
            subset_df[ticker].values[-1],
            color=line_color,
            s=point_size,
        )
    if "area" in elements_to_draw:
        ax.fill_between(subset_df["Date"], subset_df[ticker], alpha=0.3)

    # custom axes style
    ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))
    ax.set_ylim(0, subset_df[ticker].max() * 1.1)

    # annotate the last point
    ax_text(
        subset_df["Date"].values[-1],
        subset_df[ticker].values[-1] * 1.06,
        f"{subset_df[ticker].values[-1]:,.0f}",
        color=line_color,
        fontsize=12,
        ha="right",
        va="center",
        ax=ax,
    )

    # title
    fig_text(x=0.15, y=0.96, s=title, fontsize=30, ha="left")

    # copyright annotations
    fig_text(
        x=0.5,
        y=0.8,
        s="COPYRIGHT\nCOPYRIGHT\nCOPYRIGHT",
        color="grey",
        ha="center",
        fontsize=50,
        fontweight="bold",
        rotation=-15,
        alpha=0.4,
    )

    return ax
