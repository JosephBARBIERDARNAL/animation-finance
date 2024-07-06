import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.ui import spacing, header
from src.data import load_yahoo_data
from src.animation import update

header()

st.markdown("### Select the company")

# select ticker
ticker = st.selectbox(
    "Ticker", options=["AAPL", "GOOGL", "MSFT"], key="ticker selection"
)
df = load_yahoo_data(ticker).tail(20)
st.dataframe(df)

spacing(10)
st.markdown("### Customize style and change settings")


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

spacing(3)

col1, col2, col3, col4 = st.columns([1.2, 1, 3, 4])
with col1:
    background_color = st.color_picker("Background", value="#ffffff")
with col2:
    line_color = st.color_picker("Line", value="#6700D4")
with col3:
    spines_to_remove = st.multiselect(
        "Border to removes", options=["top", "right", "left", "bottom"]
    )
with col4:
    title = st.text_area("Title", value=f"A financial history: {ticker}")


spacing(10)


st.markdown("### Start the program")
if st.toggle("Create animation"):

    progress_text = "Creating the animation"
    my_bar = st.progress(0, text=progress_text)

    # initiate figure
    fig, axs = plt.subplots(figsize=(14, 8), dpi=dpi)
    fig.set_facecolor(background_color)
    axs.set_facecolor(background_color)
    if len(spines_to_remove) > 0:
        axs.spines[spines_to_remove].set_visible(False)

    # additional arguments for the update() function
    fargs = (df, axs, ticker, my_bar, line_color, title)

    # create and save animation
    path = f"video/anim-{ticker}.mp4"
    ani = FuncAnimation(fig, func=update, frames=len(df), fargs=fargs)
    ani.save(path, fps=fps)

    # display animation
    st.video(path, loop=True, autoplay=True, muted=True)


spacing(10)
