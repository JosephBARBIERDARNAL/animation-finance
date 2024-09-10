import streamlit as st
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

from src.ui import spacing, header, footer
from src.data import load_yahoo_data, convert_base, interpolate_data
from src.animation import make_animation
from src.tickers import company_tickers
from src.theme import light_theme, dark_theme


@st.cache_data(show_spinner=False)
def load_and_process_data(tickers, n_wanted, interpolate=False, interpolation_factor=1):
    df = load_yahoo_data(tickers)
    df = df.tail(n_wanted).reset_index()
    for ticker in tickers:
        df[ticker] = convert_base(df[ticker])
    if interpolate:
        df = interpolate_data(df, factor=interpolation_factor)
    return df


@st.cache_resource(show_spinner=False)
def create_animation(
    df, tickers, figsize, dpi, fps, title, elements_to_draw, theme, output_format
):
    fig, axs = plt.subplots(figsize=figsize, dpi=dpi)
    fig.set_facecolor(theme["background-color"])
    axs.spines[["top", "right", "bottom"]].set_visible(False)

    my_bar = st.progress(0, text="Creating the animation")
    fargs = (
        df,
        axs,
        fig,
        tickers,
        my_bar,
        title,
        elements_to_draw,
        theme,
        output_format,
    )

    path = f"video/{'_'.join(tickers)}.mp4"
    if not os.path.exists("video"):
        os.makedirs("video")

    ani = FuncAnimation(fig, func=make_animation, frames=len(df), fargs=fargs)
    ani.save(path, fps=fps, writer="ffmpeg")
    plt.close(fig)
    return path


header()

st.html(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important;
        }
    </style>
    """
)

tickers = st.multiselect(
    "Select the ticker's company",
    options=company_tickers.keys(),
    default="AAPL",
    key="ticker selection",
)
if len(tickers) > 0:

    spacing(4)

    with st.sidebar:
        st.markdown("## Customize style and change settings")
        spacing(4)

        st.markdown("##### Animation parameters")
        dpi = st.slider(
            "Select the resolution",
            min_value=30,
            max_value=500,
            value=300,
        )
        fps = st.slider(
            "Select FPS (frames per second, the higher the value, the faster the video)",
            min_value=1,
            max_value=100,
            value=15,
            help="A higher FPS leads to a faster video.",
        )

        spacing(4)
        st.markdown("##### Style parameters")
        col1, col2 = st.columns(2)
        with col1:
            theme_string = st.selectbox("Theme", options=["Light", "Dark"], index=0)
            theme = light_theme if theme_string == "Light" else dark_theme

        with col2:
            options_format_video = ["Square", "Landscape", "Portrait"]
            output_format = st.selectbox("Output format", options=options_format_video)
            figsize = {
                "Landscape": (12.8, 7.2),
                "Portrait": (7.2, 12.8),
                "Square": (7.2, 7.2),
            }.get(output_format, (7.2, 7.2))

        spacing(4)
        st.markdown("##### Chart parameters")
        elements_to_draw = st.multiselect(
            "Choose elements to put on the chart",
            options=["line", "final point", "area"],
            default=["line", "final point"],
        )
        if "line" not in elements_to_draw:
            st.warning("It's probably a bad idea to remove the lines from your chart.")
        title = st.text_input("Title", value="A financial history")

        spacing(4)
        st.markdown("##### Data parameters")

        n_wanted = st.slider("Number of points", min_value=10, max_value=1000, value=30)

        interpolate = st.toggle("Interpolate")
        interpolation_factor = 1
        if interpolate:
            interpolation_factor = st.slider(
                "Factor of interpolation",
                min_value=1,
                max_value=10,
                value=3,
                help="An interpolation factor of 3 means that the data has 3 times more data points. Warning: the higher this value, the longer the video will take to create.",
            )
        df = load_and_process_data(tickers, n_wanted, interpolate, interpolation_factor)
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
            st.error(
                f"End date ({end_date}) cannot be before start date ({start_date})"
            )

    st.markdown("### Start the program")

    create_anim = st.toggle("Create animation")

    if create_anim:
        if end_date < start_date:
            raise ValueError(
                f"Unexpected input: start date ({start_date}) is after end date ({end_date})"
            )

        message = random.choice(
            [
                "How about making some coffee while the program runs?",
                "Have you drunk enough water today? Take this time to have a glass.",
                "Damn, I forgot how boring waiting can be sometimes.",
                "Stretch your legs a bit. It's good for your health.",
                "Maybe a quick walk? Refresh your mind.",
                "Perfect time for a short break. You deserve it.",
            ]
        )
        st.write(message)

        video_path = create_animation(
            df,
            tickers,
            figsize,
            dpi,
            fps,
            title,
            elements_to_draw,
            theme,
            output_format,
        )

        st.video(video_path, loop=True, autoplay=True, muted=True)

        with open(video_path, "rb") as file:
            btn = st.download_button(
                label="Download video",
                data=file,
                file_name=f"{video_path.split('/')[-1]}",
                mime="video/mp4",
            )

spacing(20)
footer()
