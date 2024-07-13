import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.ui import spacing, header, footer
from src.data import load_yahoo_data, convert_base, interpolate_data
from src.animation import update, make_animation
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
    # if len(tickers) > 1:
    #     tickers = tickers[0]

    spacing(4)

    with st.sidebar:
        st.markdown("## Customize style and change settings")
        spacing(4)

        st.markdown("##### Animation parameters")
        # choose DPI
        dpi = st.slider(
            "Select the resolution (the higher the resolution, the better the video, but the longer it takes to create)",
            min_value=30,
            max_value=500,
            value=100,
            help="A higher resolution leads to more time to create the animation.",
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
            output_format = st.selectbox(
                "Output format",
                options=["Mobile", "Desktop"],
            )
            if output_format == "Mobile":
                figsize = (10, 19)
            elif output_format == "Desktop":
                figsize = (19, 10)
        font_name = st.selectbox("Font", options=["AbhayaLibre", "Sarabun", "Caladea"])

        spacing(4)
        st.markdown("##### Chart parameters")
        elements_to_draw = st.multiselect(
            "Choose elements to put on the chart",
            options=["line", "final point", "area"],
            default=["line", "final point", "area"],
        )

        spacing(4)
        st.markdown("##### Data parameters")
        base = st.toggle("Use base 100 format (recommended)", value=True)
        title = st.text_input("Title", value=f"A financial history")
        description = st.text_area(
            "Description",
            value="The description is supposed to be a large text that will appears throughout the video. Hope it renders well",
        )

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
            df = interpolate_data(df)

        st.dataframe(df)

    st.markdown("### Start the program")

    col1, col2 = st.columns(2)
    with col1:
        create_anim = st.toggle("Create animation")
    if create_anim:

        if end_date < start_date:
            raise ValueError(
                "Unexpected input: start date ({start_date}) is after end date ({end_date})"
            )

        # initialize the progress bar
        progress_text = "Creating the animation"
        my_bar = st.progress(0, text=progress_text)

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
            description,
            elements_to_draw,
            theme,
            output_format,
            font_name,
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
