import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.ui import spacing
from src.data import load_yahoo_data
from src.animation import update

st.title("Animation for finance")

ticker = st.selectbox(
    "Ticker", options=["AAPL", "GOOGL", "MSFT"], key="ticker selection"
)
df = load_yahoo_data(ticker).head(30)
st.dataframe(df.head())

fig, axs = plt.subplots(figsize=(14, 10), dpi=300)

if st.toggle("Create animation"):

    # create and save animation
    path = f"video/anim-{ticker}.mp4"
    ani = FuncAnimation(fig, func=update, frames=len(df), fargs=(df, axs, ticker))
    ani.save(path, fps=20)

    # display animation
    st.video(path)
