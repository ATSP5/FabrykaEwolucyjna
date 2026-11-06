import math

import pandas as pd


class PolishNumberFormat:
    """Polish number notation: a space between thousands and a comma before the decimals."""

    def __init__(self, decimals: int = 2, thousands: str = " ", decimal: str = ","):
        if decimals < 0:
            raise ValueError("decimals must not be negative")
        if not thousands or not decimal or thousands == decimal:
            raise ValueError("thousands and decimal separators must be two different characters")
        self.decimals = decimals
        self.thousands = thousands
        self.decimal = decimal

    def number(self, value, decimals: int = None, signed: bool = False) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ""
        digits = self.decimals if decimals is None else decimals
        text = format(float(value), ("+" if signed else "") + ",.%df" % digits)
        return text.replace(",", "\0").replace(".", self.decimal).replace("\0", self.thousands)

    def percent(self, value, decimals: int = 2, signed: bool = False) -> str:
        return self.number(value, decimals, signed) + " %"

    def frame(self, frame: pd.DataFrame, decimals=None) -> pd.DataFrame:
        """A copy with every numeric column as text; decimals is one int or {column: int}."""
        shown = frame.copy()
        for name in shown.columns:
            if not pd.api.types.is_numeric_dtype(shown[name]):
                continue
            digits = decimals.get(name, self.decimals) if isinstance(decimals, dict) else decimals
            shown[name] = [self.number(value, digits) for value in shown[name]]
        return shown

    def plotly_layout(self, y_title: str = None, x_title: str = None, y_decimals: int = 0) -> dict:
        """Plotly layout keys that draw axes and hover labels in the same notation."""
        return {
            "separators": self.decimal + self.thousands,
            "yaxis": {"title": {"text": y_title}, "tickformat": ",.%df" % y_decimals, "automargin": True},
            "xaxis": {"title": {"text": x_title}, "automargin": True},
        }

    def hover(self, unit: str = "", decimals: int = 0, axis: str = "y") -> str:
        """A Plotly hovertemplate showing the value with its unit and the series name."""
        return "%%{x}: %%{%s:,.%df} %s<extra>%%{fullData.name}</extra>" % (axis, decimals, unit)

    def formatter(self):
        return self
