import marimo

__generated_with = "0.9.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return mo, pd, plt


@app.cell
def _(pd):
    df = pd.read_csv("data/features/events.csv")
    df
    return (df,)


@app.cell
def _(df, mo, plt):
    fig, ax = plt.subplots()
    ax.hist(df["duration_minutes"], bins=40)
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Event Durations")
    mo.mpl.interactive(fig)
    return ax, fig


if __name__ == "__main__":
    app.run()
