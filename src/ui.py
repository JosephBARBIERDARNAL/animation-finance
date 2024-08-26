import streamlit as st


def spacing(n: int):
    for _ in range(n):
        st.write("")


def header(marginBottom=2):
    st.html("<center><h2>Stock motion</h2></center>")
    st.html(
        "<center><p style='font-size:20px;'>Turning Market Data into Dynamic Visuals</p></center>"
    )
    spacing(marginBottom)


def footer():
    st.html(
        "<center>A project by <a href='https://barbierjoseph.com/'>Joseph Barbier</a></center>"
    )
