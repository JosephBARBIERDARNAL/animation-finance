import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.utils import generate_id
from src.ui import spacing, header, footer
from src.data import load_yahoo_data
from src.animation import update

header()

spacing(15)
st.markdown("### Customize style and change settings")

# select ticker
ticker = st.multiselect(
    "Ticker", options=["AAPL", "GOOGL", "MSFT"], default="AAPL", key="ticker selection"
)


spacing(4)
st.markdown("##### Animation parameters")
col1, col2 = st.columns([1, 1])
with col1:
    # choose DPI
    dpi = st.slider(
        "Select resolution",
        min_value=30,
        max_value=300,
        value=100,
        help="A higher resolution leads to more time to create the animation.",
    )
with col2:
    # choose FPS
    fps = st.slider(
        "Select FPS (frame per second)",
        min_value=1,
        max_value=100,
        value=15,
        help="A higher FPS leads to a faster video.",
    )

spacing(4)
st.markdown("##### Style parameters")
col1, col2 = st.columns(2)
with col1:
    background_color = st.color_picker("Background", value="#ffffff")
with col2:
    line_color = st.color_picker("Line", value="#000000")

spines_to_remove = st.multiselect(
    "Border to remove",
    options=["top", "right", "left", "bottom"],
    default=["top", "right"],
)

spacing(4)
st.markdown("##### Chart parameters")
elements_to_draw = st.multiselect(
    "Choose elements to put on the chart",
    options=["line", "final point", "area"],
    default=["line", "final point", "area"],
)
col1, col2 = st.columns(2)
with col1:
    if "line" in elements_to_draw:
        linewidth = st.slider("Linewidth", min_value=0.1, max_value=10.0, value=3.0)
    else:
        linewidth = 3.0
with col2:
    if "final point" in elements_to_draw:
        point_size = st.slider("Point size", min_value=1, max_value=1000, value=300)
    else:
        point_size = 300

spacing(4)
st.markdown("##### Data parameters")
base = st.toggle("Use base 100 format (recommended)", value=True)
title = st.text_area("Title", value=f"A financial history: {ticker}")
if base:
    title += f" (base 100)"

df = load_yahoo_data(ticker, base=base).head(500)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start date",
        min_value=df["Date"].min(),
        max_value=df["Date"].max(),
        value=df["Date"].min(),
        key="startdate",
    )
with col2:
    end_date = st.date_input(
        "End date",
        min_value=df["Date"].min(),
        max_value=df["Date"].max(),
        value=df["Date"].max(),
        key="endate",
    )
if end_date < start_date:
    st.error(f"End date ({end_date}) cannot be before start date ({start_date})")


spacing(15)


st.markdown("### Start the program")
if st.toggle("Create animation") and end_date > start_date:

    # initialize the progress bar
    progress_text = "Creating the animation"
    my_bar = st.progress(0, text=progress_text)

    # initiate figure
    fig, axs = plt.subplots(figsize=(14, 8), dpi=dpi)
    fig.set_facecolor(background_color)
    axs.set_facecolor(background_color)
    if len(spines_to_remove) > 0:
        axs.spines[spines_to_remove].set_visible(False)

    # additional arguments for the update() function
    fargs = (
        df,
        axs,
        ticker,
        my_bar,
        line_color,
        title,
        elements_to_draw,
        linewidth,
        point_size,
    )

    # create and save animation
    video_id = generate_id(10)
    video_id = "no_id_yet"
    path = f"video/{ticker}-{video_id}.mp4"
    ani = FuncAnimation(fig, func=update, frames=len(df), fargs=fargs)
    ani.save(path, fps=fps)

    # display animation
    st.video(path, loop=True, autoplay=True, muted=True)

    # save button
    with open(path, "rb") as file:
        btn = st.download_button(
            label="Download video",
            data=file,
            file_name=f"{path.split('/')[-1]}",
            mime="image/png",
        )


spacing(20)
footer()
