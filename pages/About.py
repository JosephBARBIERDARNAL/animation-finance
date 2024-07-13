from src.ui import spacing, header, footer
import streamlit as st

header()

st.html(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
    </style>
    """
)

st.markdown(
    """
## Open source

This project is entirely [open source](https://github.com/JosephBARBIERDARNAL/animation-finance). You can report bugs, suggest and develop new features using the [Github repository](https://github.com/JosephBARBIERDARNAL/animation-finance).

Contributions and feedback are welcome! 😁

## How it works

The core of the app relies on `yfinance` for loading the data, and then uses `matplotlib` to create a figure that will be updated at each date thanks to its `FuncAnimation` component. The UI is made via `streamlit`.
"""
)


spacing(20)
footer()
