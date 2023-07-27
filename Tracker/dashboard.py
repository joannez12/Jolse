from dash.exceptions import PreventUpdate
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from Pipeline.Pipeline.connection import connect_db

engine = connect_db()

products = pd.read_sql_query('select name from product order by name', con=engine)['name'].tolist()
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Jolse Products", ),
        html.Div(
            children=[
                html.Div(children="Products List", className="menu-title"),
                dcc.Dropdown(
                    id="product-filter",
                    options=[
                        {"label": product, "value": product}
                        for product in products
                    ],
                    # value=products[0],
                    placeholder="Select a product",
                    # clearable=False,
                    className="dropdown",
                ),
            ]
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output("price-chart", "figure"),
    Input("product-filter", "value"),
)

def update_charts(product):
    if not product:
        raise PreventUpdate
    filtered_data = pd.read_sql_query(
        'select * from price join product on price.item_id=product.id where product.name=' + '\'' + product + '\' order by date',
        con=engine)
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["sale_price"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Price of " + product,
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "date", "fixedrange": True},
            "yaxis": {"title": "price (USD)", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return price_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)