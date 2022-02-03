"""Formatting different type of data output into HTML."""
import re

import numpy as np
import pandas as pd


def _pandas_dataframe_to_html_initial_set_up(
    data: pd.DataFrame,
    index: bool = False,
):
    if not index:
        data.reset_index(drop=True, inplace=True)
        plus_number = 1
    else:
        plus_number = 2
    return data, plus_number


def _pandas_dataframe_to_html_percentage(
    data: pd.DataFrame, percentage_col: list = None
):
    for col in percentage_col if percentage_col else []:
        if col in list(data):
            data[col] = f"{(100.0 * data[col]).round(1).astype(str)}%"
    return data


def _pandas_dataframe_to_html_special_numbers(data_html: str):
    for _ in ["nan%", "inf%", "-inf%", "nan", "inf", "-inf"]:
        data_html = re.sub(_, "", data_html)
    return data_html


def _pandas_dataframe_to_html_set_width(
    data_html: str,
    width_col: dict = None,
):
    for key, value in width_col.items() if width_col else {}.items():
        data_html = re.sub(
            f'<th>{key}<th style="width: {value}>">{key}', data_html
        )
    return data_html


def _pandas_dataframe_to_html(
    data: pd.DataFrame,
    numeric_format: str = "{:20.2f}",
    numeric_align: str = "right",
    percentage_col: list = None,
    width_col: dict = None,
    table_style: str = "table",
    table_sub_style: str = "table-striped",
    table_font_size: str = "table-sm",
    index: bool = False,
):
    """Convert pandas dataframe to html output.

    Args:
        data (pd.DataFrame): Data to be formatted.
        numeric_format (str, optional):
            Set up format for numerical data. Defaults to "{:20.0f}".
        numeric_align (str, optional):
            Set default alignment for numerical data. Defaults to "right".
        percentage_col (list, optional):
            List of column names to be percenrage output. Defaults to None.
        width_col (dict, optional):
            Provide key as column name and vale as desired column width.
            Defaults to None.
        table_style (str, optional): HTML table style. Defaults to "table".
        table_sub_style (str, optional):
            HTML table style. Defaults to "table-striped".
        table_font_size (str, optional):
            HTML table style. Defaults to "table-sm".
        index (bool, optional):
            Determine if dropping index. Defaults to False.
    """
    data = data.copy()
    data, plus_number = _pandas_dataframe_to_html_initial_set_up(
        data=data, index=index
    )
    data_type = data.dtypes.tolist()
    align_right_list = [
        f"col{str(idx+plus_number)}-{numeric_align}"
        for idx, val in enumerate(data_type)
        if val != np.object
    ]
    align_right_str = (
        f"<table class='{table_style} {table_font_size} {table_sub_style} "
        f"{' '.join(align_right_list)} '>"
    )
    data = _pandas_dataframe_to_html_percentage(
        data=data, percentage_col=percentage_col
    )
    data.columns = [c.replace("_", " ") for c in data.columns]
    data_html = re.sub(
        r'\<table border="1" class="dataframe table table-bordered">',
        align_right_str,
        data.to_html(
            classes="table table-bordered",
            float_format=numeric_format.format,
            index=index,
        ),
    )
    data_html = _pandas_dataframe_to_html_special_numbers(data_html=data_html)
    data_html = _pandas_dataframe_to_html_set_width(
        data_html=data_html, width_col=width_col
    )
    return data_html
