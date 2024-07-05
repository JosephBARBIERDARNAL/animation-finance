from highlight_text import fig_text

text = """<Global plastics production has grown dramatically and is set to continue to do so>
<Evolution and prediction of annual plastic production>
<Data after 2020 are predicted values based on a polynomial regression>
"""
fig_text(
    0.13,
    0.92,
    text,
    ha="left",
    va="top",
    font=font,
    highlight_textprops=[
        {"color": text_color, "fontsize": 14, "font": bold_font},
        {"color": text_color, "fontsize": 10},
        {"color": text_color, "fontsize": 10},
    ],
    fig=fig,
)

# credit annotation
text = """
Developed by <@joseph_barbier>
"""
fig_text(
    0.9,
    0,
    text,
    ha="right",
    va="bottom",
    fontsize=7,
    font=font,
    color=text_color,
    highlight_textprops=[
        {"font": bold_font},
    ],
    fig=fig,
)
