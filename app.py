"""
Dash app visualising Pink Morsel sales over time to answer:
Were sales higher before or after the price increase on 15 Jan 2021?
"""
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

DATA_FILE = "data/formatted_sales_data.csv"
PRICE_INCREASE_DATE = "2021-01-15"

# Load and prepare data
df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Sum sales across all regions for each date so the trend is easy to read
daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={"Date": "Date", "Sales": "Sales ($)"},
)
fig.add_vline(
    x=PRICE_INCREASE_DATE,
    line_dash="dash",
    line_color="red",
    annotation_text="Price increase (15 Jan 2021)",
    annotation_position="top",
)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Soul Foods: Pink Morsel Sales Visualiser"),
        dcc.Graph(id="sales-line-chart", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)