from typing import List, Tuple
import pandas as pd
from pandas import DataFrame
import numpy as np
from colorcet import b_glasbey_bw
from loguru import logger
import math


def filter_by_ranges(
    data: DataFrame, filter_column: str, ranges: List[Tuple[float, float]]
) -> DataFrame:

    frames = []

    for r in ranges:
        frames.append(data[data[filter_column].between(r[0], r[1])])

    return pd.concat(frames)


def get_ranges(
    data: DataFrame, from_column: str, to_column: str
) -> List[Tuple[float, float]]:
    return list(zip(data[from_column], data[to_column]))


def get_data_frame_from_file(filepath: str, ignore_rows: List[int] = None) -> DataFrame:
    if ignore_rows is not None and len(ignore_rows) == 0:
        ignore_rows = None

    try:
        if ".csv" in filepath.lower():
            # Assume that the user uploaded a CSV file
            return pd.read_csv(filepath, skiprows=ignore_rows)
        elif ".xls" in filepath.lower():
            # Assume that the user uploaded an excel file
            return pd.read_excel(filepath, skiprows=ignore_rows)
    except Exception as e:
        raise Exception("{} couldn't be parsed error: {}".format(filepath, str(e)))


def filter_data_by_ranges_from_file(
    data_file: str,
    filter_file: str,
    from_column: str,
    to_column: str,
    filter_column: str,
    output_file: str,
):

    data_df = get_data_frame_from_file(data_file)
    filter_df = get_data_frame_from_file(filter_file)

    assert (
        from_column in filter_df.columns
    ), f"Column {from_column} not in {filter_file}"
    assert to_column in filter_df.columns, f"Column {to_column} not in {filter_file}"
    assert (
        filter_column in data_df.columns
    ), f"Column {filter_column} not in {data_file}"

    ranges = get_ranges(filter_df, from_column, to_column)
    filtered_df = filter_by_ranges(data_df, filter_column, ranges)

    filtered_df.sort_values(by=[filter_column], inplace=True)

    if ".xls" not in output_file:
        output_file += ".xlsx"

    filtered_df.to_excel(output_file, index=False)


def get_median_gap(df: pd.DataFrame, from_col: str, to_col: str) -> float:
    """Shift the from column down to calculate the median gap size

    Args:
        df (pd.DataFrame): [description]
        from_col (str): [description]
        to_col (str): [description]

    Returns:
        float: [description]
    """
    temp_df = df[[from_col, to_col]]
    from_shift = temp_df[from_col].shift(-1)
    temp_df.drop(df.tail(1).index, inplace=True)
    from_shift.drop(from_shift.tail(1).index, inplace=True)
    return (from_shift - temp_df[to_col]).median()


def add_gap_rows(df: pd.DataFrame, insert_at: List[dict]):
    df_new = pd.DataFrame(columns=df.columns)
    counter = 0
    for idx in range(len(df)):
        if len(insert_at) > counter and insert_at[counter]['index'] == idx:
            df_new = df_new.append(pd.Series(), ignore_index=True)
            df_new.iloc[-1, df_new.columns.get_loc('depth')] = insert_at[counter]['depth']
            counter += 1
        df_new = df_new.append(df.iloc[idx])
    return df_new


def down_hole_signal_plots(
    data_file: str,
    y_column: str = None,
    from_column: str = None,
    to_column: str = None,
    var_columns: List[str] = None,
    output_file: str = "output.html",
    colours: List[str] = b_glasbey_bw,
    ignore_rows: List[int] = None
):

    data_df = get_data_frame_from_file(data_file, ignore_rows)
    plot_type = "line"

    if var_columns is None:
        var_columns = data_df.select_dtypes(include=np.number).columns.tolist()

        if len(var_columns) == 0:
            logger.error(f"No numeric columns detected in {data_file}")
            return

    # assert var_columns in data_df.columns, f"One or more of {str(var_columns)} not in {data_file}"
    widths = None

    if None not in [from_column, to_column]:
        assert (
            from_column in data_df.columns
        ), f"Column {from_column} not in {data_file}"
        assert to_column in data_df.columns, f"Column {to_column} not in {data_file}"

        var_columns.remove(from_column)
        var_columns.remove(to_column)
        data_df = data_df.sort_values(from_column, ascending=True)

        data_df["depth"] = data_df[[from_column, to_column]].mean(axis=1)
        data_df["widths"] = (data_df[to_column] - data_df[from_column])

        # FIXME Gaps currently don't work due to a plotly bug https://github.com/plotly/plotly.js/issues/1132
        # Calculate the median gap size
        # median_gap = get_median_gap(data_df, from_column, to_column)

        # depth_diff = data_df["depth"].diff()

        # gap_indexes = []
        # for i, diff in enumerate(depth_diff):
        #     if diff is not np.NaN and diff > median_gap * 2:
        #         gap_indexes.append({'index': i, 'depth': (diff/2 + data_df.at[i-1, "depth"])}),

        # data_df = add_gap_rows(data_df, gap_indexes)
        y_column = "depth"
    else:
        assert y_column in data_df.columns

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    cols = len(var_columns)
    rows = 1
    print(f"Cols = {cols}")

    if cols > 100:
        cols = math.ceil(cols / 2.0)
        rows = 2

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=var_columns,
        horizontal_spacing=0.003,
        vertical_spacing=0.1,
        shared_yaxes=True,
        y_title="",
    )

    for i, column in enumerate(var_columns):
        i_col = i + 1

        row = 2 if i_col > cols else 1
        col = i_col - cols if i_col > cols else i_col

        # data = data_df[column].to_list()
        # data = [None if math.isnan(d) else d for d in data]

        if plot_type == "bar":
            fig.add_trace(go.Bar(
                x=data_df[column],
                y=data_df[y_column].to_list(),
                width=widths,
                marker_color=colours[i] if len(colours) > i else colours[0],
                orientation='h',
                # base=math.floor(data_df[column].min()),
                showlegend=False,
                hovertemplate="<br>Value: %{x} </br>Depth/Sample: %{y}"), row=row, col=col)
        else:
            fig.add_trace(go.Scatter(
                x=data_df[column],
                y=data_df[y_column].to_list(),
                mode='lines+markers',
                fill='tozerox',
                marker_color=colours[i] if len(colours) > i else colours[0],
                orientation='h',
                # base=math.floor(data_df[column].min()),
                showlegend=False,
                connectgaps=False,
                hovertemplate="<br>Value: %{x} </br>Depth/Sample: %{y}"), row=row, col=col)

        fig.update_xaxes(range=[0, data_df[column].max()], row=row, col=col)

    fig.update_layout(
        title={
            'text': data_file,
            'x': 0,
            'y': 1,
        },
        # template='simple_white',
        margin={"r": 0, "t": 130, "l": 120, "b": 20},
        # plot_bgcolor="White",
        autosize=True,
        hovermode="closest",
        width=50 * cols + 150,
        height=1200,
    )

    fig.update_yaxes(
        # range=[mosaic_df.ymax.max(), mosaic_df.ymin.min()],
        matches="y",
        mirror=True,
        showline=True,
        # showgrid=True,
        linecolor='black',
        autorange="reversed",
    )

    fig.update_xaxes(
        # matches='x',
        showline=True,
        mirror=True,
        linecolor='black',
        nticks=2,
        zerolinewidth=1,
        zerolinecolor='Black',
        tickangle=90
    )

    for annotation in fig['layout']['annotations']:
        annotation['textangle'] = -60

    config = dict({'displayModeBar': True})

    fig.write_html(output_file, config=config)
