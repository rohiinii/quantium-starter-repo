"""
Dash app visualising Pink Morsel sales over time to answer:
Were sales higher before or after the price increase on 15 Jan 2021?
Includes a region filter and custom styling.
"""
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA_FILE = "data/formatted_sales_data.csv"
PRICE_INCREASE_DATE = "2021-01-15"

# Load and prepare data
df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")


def build_figure(region: str):
    """Build the line chart, optionally filtered to a single region."""
    filtered = df if region == "all" else df[df["Region"] == region]
    daily_sales = filtered.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": "Sales ($)"},
        title=f"Pink Morsel Sales Over Time — {region.title()}",
    )
    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash="dash",
        line_color="#e74c3c",
        annotation_text="Price increase (15 Jan 2021)",
        annotation_position="top",
    )
    fig.update_traces(line_color="#6c5ce7", line_width=3)
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font_family="Helvetica, Arial, sans-serif",
        title_font_size=20,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig


app = Dash(__name__)

app.layout = html.Div(
    className="app-container",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("🍬 Soul Foods: Pink Morsel Sales Visualiser"),
                html.P("Explore Pink Morsel sales before and after the price increase."),
            ],
        ),
        html.Div(
            className="controls",
            children=[
                html.Label("Filter by region:", className="controls-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                        {"label": "All", "value": "all"},
                    ],
                    value="all",
                    inline=True,
                    className="radio-group",
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[dcc.Graph(id="sales-line-chart", figure=build_figure("all"))],
        ),
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    return build_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)
