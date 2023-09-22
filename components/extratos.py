import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
               id='bar-graph',
               style={'margin-right': '20px'}
            )
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.Legend(
                        'R$ 4400',
                        id='expense-value-card',
                        style={'font-size': '60px', 'font-weight': 'bold'}
                    ),
                    html.H6('Total de despesas')
                ], style={'text-align': 'left', 'padding-top': '30px'})
            )
        ], width=3)
    ])
], style={'padding': '10px'})

# =========  Callbacks  =========== #
# Update graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('store-expense', 'data')]
)
def show_graph(data):
    df = pd.DataFrame(data)
    df_grouped = df.groupby('Categoria').sum()[['Valor']].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title='Despesas Gerais')
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return graph

# Update expense total balance
@app.callback(
    Output('expense-value-card', 'children'),
    Input('store-expense', 'data')
)
def update_balance(data):
    df = pd.DataFrame(data)
    value = df['Valor'].sum()
    return f'R$ {value}'