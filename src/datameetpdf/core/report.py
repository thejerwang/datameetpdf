"""Main class to create PDF reports."""
import os
from dataclasses import dataclass

import pandas as pd
import pdfkit

from datameetpdf.template.basic_html import _basic_html
from datameetpdf.util.html import _pandas_dataframe_to_html

BASIC_CSS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "template",
    "basic.css",
)


@dataclass
class ReportItem:
    """Class for keeping track of an item in report."""

    item_type: str
    formatted_data: str
    title: str = None


class ReportCreation:
    """Create PDF report."""

    def __init__(
        self, css_template: str = BASIC_CSS, path: str = None, *args, **kwargs
    ) -> None:
        """Pass basic setting by init."""
        self.css_template = css_template
        self.options = {
            "page-size": kwargs.get("page-size", "A4"),
            "dpi": kwargs.get("dpi", 400),
            "margin-top": kwargs.get("margin-top", "0.5in"),
            "margin-right": kwargs.get("margin-right", "0.5in"),
            "margin-bottom": kwargs.get("margin-bottom", "0.5in"),
            "margin-left": kwargs.get("margin-left", "0.5in"),
        }
        self.path = path
        self.report_items = []

    def add_dataframe(
        self,
        data: pd.DataFrame,
        title: str = None,
        numeric_format: str = "{:20.2f}",
        numeric_align: str = "right",
        percentage_col: list = None,
        width_col: dict = None,
        table_style: str = "table",
        table_sub_style: str = "table-striped",
        table_font_size: str = "table-sm",
        index: bool = False,
    ) -> None:
        """Add dataframe to the report.

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
        self.report_items += [
            ReportItem(
                item_type="dataframe",
                formatted_data=_pandas_dataframe_to_html(
                    data=data,
                    numeric_format=numeric_format,
                    numeric_align=numeric_align,
                    percentage_col=percentage_col,
                    width_col=width_col,
                    table_style=table_style,
                    table_sub_style=table_sub_style,
                    table_font_size=table_font_size,
                    index=index,
                ),
                title=title,
            )
        ]

    def generate_pdf(self):
        """Generate PDF."""
        body_str = ""
        for item in self.report_items:
            if item.title:
                body_str += f"<h5><b>{item.title}</b></h5>"
            body_str += item.formatted_data
        pdfkit.from_string(
            input=_basic_html(body_str=body_str),
            output_path=self.path,
            css=self.css_template,
            options=self.options,
        )
