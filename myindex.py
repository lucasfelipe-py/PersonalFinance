import dash
from dash import html, dcc 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import sidebar, dashboards, extratos

from globals import *


# ========= Layout ========= #
content = html.Div(id='page-content')

app.layout = dbc.Container(children=[
    # Sharing data between callbacks
    dcc.Store(id='store-revenue', data=df_revenue.to_dict()),
    dcc.Store(id='store-expense', data=df_expense.to_dict()),
    dcc.Store(id='store-cat-revenue', data=df_cat_revenue.to_dict()),
    dcc.Store(id='store-cat-expense', data=df_cat_expense.to_dict()),
    
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'), # Page id
            sidebar.layout
        ], md=2),
        
        dbc.Col([
            content
        ], md=10)
    ])
], fluid=True)

# ========= Callbacks ========= #
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page(pathname):
    if pathname == '/' or pathname == '/dashboards':
        return dashboards.layout
    if pathname == '/extratos':
        return extratos.layout

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)