import streamlit as st
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.ui import spacing, header, footer
from src.data import load_yahoo_data, convert_base, interpolate_data
from src.animation import make_animation
from src.tickers import company_tickers
from src.theme import light_theme, dark_theme

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


# select ticker
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
        # choose DPI
        dpi = st.slider(
            "Select the resolution",
            min_value=30,
            max_value=500,
            value=300,
        )
        # choose FPS
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
            if theme_string == "Light":
                theme = light_theme
            elif theme_string == "Dark":
                theme = dark_theme

        with col2:
            options_format_video = [
                "Landscape",
                "Portrait",
                "Square",
            ]
            output_format = st.selectbox(
                "Output format",
                options=options_format_video,
            )
            if output_format == "Landscape":
                figsize = (12.8, 7.2)
            elif output_format == "Portrait":
                figsize = (7.2, 12.8)
            elif output_format == "Square":
                figsize = (7.2, 7.2)
            else:
                st.stop("some bug in the matrix")

        spacing(4)
        st.markdown("##### Chart parameters")
        elements_to_draw = st.multiselect(
            "Choose elements to put on the chart",
            options=["line", "final point", "area"],
            default=["line", "final point", "area"],
        )
        if "line" not in elements_to_draw:
            st.warning("It's probably a bad idea to remove the lines from your chart.")
        title = st.text_input("Title", value="A financial history")

        spacing(4)
        st.markdown("##### Data parameters")
        base = st.toggle("Use base 100 format (recommended)", value=True)

        df = load_yahoo_data(tickers)
        n_wanted = st.slider(
            "Number of points", min_value=10, max_value=len(df), value=30
        )
        df = df.tail(n_wanted).reset_index()
        if base:
            for ticker in tickers:
                df[ticker] = convert_base(df[ticker])

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

        if st.toggle("Interpolate"):
            interpolation_factor = st.slider(
                "Factor of interpolation",
                min_value=1,
                max_value=10,
                value=3,
                help="An interpolation factor of 3 means that the data has 3 times more data points. Warning: the higher this value, the longer the video will take to create.",
            )
            df = interpolate_data(df, factor=interpolation_factor)

    st.markdown("### Start the program")

    create_anim = st.toggle("Create animation")
    if create_anim:

        if end_date < start_date:
            raise ValueError(
                "Unexpected input: start date ({start_date}) is after end date ({end_date})"
            )

        # initialize the progress bar
        progress_text = "Creating the animation"
        my_bar = st.progress(0, text=progress_text)

        # some cool message
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

        # initiate figure
        fig, axs = plt.subplots(figsize=figsize, dpi=dpi)
        fig.set_facecolor(theme["background-color"])
        axs.spines[["top", "right", "bottom"]].set_visible(False)

        # additional arguments for the update() function
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

        path = f"video/{tickers}.mp4"
        ani = FuncAnimation(fig, func=make_animation, frames=len(df), fargs=fargs)
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
