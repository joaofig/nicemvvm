from io import BytesIO

import pandas as pd
from nicegui import ui


def export_to_excel(data: list[dict], filename="data.xlsx"):
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)
    ui.download.content(output.getvalue(), filename=filename)
