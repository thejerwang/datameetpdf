"""Test report class."""
import os

import pandas as pd

from datameetpdf.core.report import ReportCreation

import plotly


def test_report_creation():
    """Test report creation."""
    data = pd.DataFrame(
        data=[
            {"name": "Jeremy", "weight": 60},
            {"name": "Karl", "weight": 80},
            {"name": "Pip", "weight": 5},
            {"name": "Squeak", "weight": 4.8},
        ]
    )
    bar = plotly.graph_objs.Bar(x=["giraffes", "orangutans", "monkeys"], y=[20, 14, 23])
    layout = plotly.graph_objs.Layout()
    plotly_fig = plotly.offline.plot(
        {"data": [bar], "layout": layout},
        show_link=False,
        output_type="div",
        include_plotlyjs=True,
    )
    rc = ReportCreation(path=os.path.join(os.getcwd(), "test.pdf"))
    rc.add_dataframe(data=data, title="J&K Family Weight Monitor")
    rc.add_next_page_break()
    rc.add_plotly(data=plotly_fig, title="Bar Chart")
    rc.generate_pdf()
