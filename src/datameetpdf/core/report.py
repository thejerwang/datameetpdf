"""Main class to create PDF reports."""
import os
from dataclasses import dataclass

import pandas as pd
import pdfkit
import plotly

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
    bold_font: bool = True
    font_size: float = 5
    underline: bool = True

    @property
    def pre_b(self) -> str:
        """Return pre string for bold."""
        return "<b>" if self.bold_font else ""

    @property
    def post_b(self) -> str:
        """Return post string for bold."""
        return "</b>" if self.bold_font else ""

    @property
    def pre_font_size_str(self) -> str:
        """Return string for font size."""
        return f"<h{self.font_size}>"

    @property
    def post_font_size_str(self) -> str:
        """Return string for font size."""
        return f"</h{self.font_size}>"

    @property
    def add_underline(self) -> str:
        """Return a line break."""
        return "<hr>" if self.underline else ""


class ReportCreation:
    """Create PDF report."""

    def __init__(
        self, css_template: str = BASIC_CSS, path: str = None, *args, **kwargs
    ) -> None:
        """Pass basic setting by init."""
        self.css_template = css_template
        self.options = {
            "javascript-delay": 1_000,
            "no-stop-slow-scripts": None,
            "debug-javascript": None,
            "page-size": kwargs.get("page-size", "A4"),
            "dpi": kwargs.get("dpi", 400),
            "margin-top": kwargs.get("margin-top", "0.5in"),
            "margin-right": kwargs.get("margin-right", "0.5in"),
            "margin-bottom": kwargs.get("margin-bottom", "0.5in"),
            "margin-left": kwargs.get("margin-left", "0.5in"),
        }
        self.path = path
        self.report_items = []
        self.body_str = ""

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
        bold_font: bool = True,
        font_size: int = 5,
        underline: bool = True,
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
            bold_font (bool, optional):
                Determine if title is bold. Defaults to True.
            font_size (int, optional):
                font size to be used. Default to be 5.
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
                bold_font=bold_font,
                font_size=font_size,
                underline=underline,
            )
        ]

    def add_plotly(
        self,
        data: plotly.graph_objs,
        title: str = None,
        bold_font: bool = True,
        font_size: int = 5,
        underline: bool = True,
    ) -> None:
        """Add plotly chart to the report."""
        self.report_items += [
            ReportItem(
                item_type="plotly",
                formatted_data=data,
                title=title,
                bold_font=bold_font,
                font_size=font_size,
                underline=underline,
            )
        ]

    def add_break(self, numbers_of_break: int = 1):
        """Add break line.

        Args:
            numbers_of_break (int, optional): Number of breaks. Defaults to 1.
        """
        self.report_items += [
            ReportItem(
                item_type="break_line",
                formatted_data="<br>" * int(numbers_of_break),
            )
        ]

    def add_next_page_break(self):
        """Add next page break."""
        self.report_items += [
            ReportItem(
                item_type="next_page",
                formatted_data='<div style = "display:block; clear:both; page-break-after:always;"></div>',
            )
        ]

    def generate_pdf(self):
        """Generate PDF."""
        for item in self.report_items:
            if item.title:
                self.body_str += (
                    f"{item.pre_font_size_str}"
                    f"{item.pre_b}"
                    f"{item.title}"
                    f"{item.post_b}"
                    f"{item.post_font_size_str}"
                    f"{item.add_underline}"
                )
            self.body_str += item.formatted_data
        pdfkit.from_string(
            input=_basic_html(body_str=self.body_str),
            output_path=self.path,
            css=self.css_template,
            options=self.options,
        )
