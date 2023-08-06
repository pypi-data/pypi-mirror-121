from glob import glob

import pandas as pd
import plotly.graph_objects as go


def get_currency_file_paths(file_dirs="data/**/*.csv"):
    """Get all currency files. Downloaded and unzipped data dumps from poe.ninja.
    :param string: file_dirs:
        The directory to search for files in. Defaults to the data dump directory.
        Defaults to csv files. If another file type is required it should be
        specified with *.filetype.

    :returns list:
        The directory and file name of each file containing the word "currency".
    """
    csv_files = [csv_file for csv_file in glob(file_dirs, recursive=True)]
    return [currency_file for currency_file in csv_files if "currency" in currency_file]


def extract_df(file_path):
    """Extracts a dataframe from a csv file path.

    :param string: file_path
        The path of a csv file.

    :returns pd.DataFrame:
        The processed and extracted dataframe for the given poe csv data.
    """
    df = pd.read_csv(
        file_path,
        sep=";",
        parse_dates=["Date"],
    )
    df.columns = df.columns.str.lower()
    df = df.rename(columns={"get": "currency"})
    df = df[df["pay"] == "Chaos Orb"]
    df = df[["league", "date", "currency", "value"]]
    return df


def get_data(file_paths):
    """Extracts and joins all the leagues from the given list of csvs.

    :param list: file_paths
        The list of the file paths to data csvs.

    :returns pd.DataFrame:
        The dataframe for all the given files.
    """
    df_list = [extract_df(file) for file in file_paths]
    df = pd.concat(df_list)
    df = df.set_index("date")
    df = df.sort_index()
    return df


def plot_currency(df):
    """Plot currency by date.

    :param pd.DataFrame: df
        The DataFrame of each currency and date.
    """

    fig = go.Figure()
    currency_list = sorted(list(df["currency"].unique()))
    fig.add_traces(
        go.Scatter(
            x=df[df["currency"] == currency_list[0]]["value"].index.values,
            y=df[df["currency"] == currency_list[0]]["value"].values,
            name=currency_list[0],
        )
    )
    updatemenus = [
        {
            "buttons": [
                {
                    "method": "restyle",
                    "label": currency,
                    "args": [
                        {"y": [df[df["currency"] == currency]["value"].values]},
                        {"x": [df[df["currency"] == currency]["value"].index.values]},
                    ],
                }
                for currency in currency_list
            ],
            "direction": "down",
            "showactive": True,
            "xanchor": "center",
            "yanchor": "bottom",
            "x": 0.5,
            "y": 1.1,
        },
    ]
    fig.update_layout(
        updatemenus=updatemenus,
        xaxis_title="Date",
        yaxis_title="Chaos Orb",
    )
    return fig
