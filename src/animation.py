def update(frame, df, ax, ticker):

    if frame == 1:
        pass

    # initialize subset of data
    subset_df = df.iloc[:frame]
    ax.clear()

    # create the line chart
    ax.plot(subset_df.index, subset_df[ticker], color="black")
    # ax.scatter(subset_df.index[-1], subset_df[ticker].values[-1], color="black", s=100)

    return ax
