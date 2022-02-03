"""Test report class."""
import os

import pandas as pd

from datameetpdf.core.report import ReportCreation


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
    rc = ReportCreation(path=os.path.join(os.getcwd(), "test.pdf"))
    rc.add_dataframe(data=data, title="J&K Family Weight Monitor")
    rc.generate_pdf()
