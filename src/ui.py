import streamlit as st


def spacing(n: int):
    for _ in range(n):
        st.write("")


def header():
    st.html("<center><h1>A financial history</h1></center>")
    st.html(
        "<center><h4>Use historical financial data to make smooth video that tells a story.</h4></center>"
    )
    spacing(6)


def footer():
    st.html(
        "<center>A project by <a href='https://barbierjoseph.com/'>Joseph Barbier</a></center>"
    )
