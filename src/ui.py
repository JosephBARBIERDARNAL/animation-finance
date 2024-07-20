import streamlit as st


def spacing(n: int):
    for _ in range(n):
        st.write("")


def header(marginBottom=2):
    st.html("<center><h2></h2></center>")
    st.html(
        "<center><p style='font-size:20px;'>Use historical financial data to make <b>smooth</b>, <b>clean</b> and <b>customizable</b> video that tells a story.</p></center>"
    )
    spacing(marginBottom)


def footer():
    st.html(
        "<center>A project by <a href='https://barbierjoseph.com/'>Joseph Barbier</a></center>"
    )
