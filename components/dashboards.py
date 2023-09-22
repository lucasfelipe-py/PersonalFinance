from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from app import app

card_icon = {
    'color': 'white',
    'textAlign': 'center',
    'fontSize': 30,
    'margin': 'auto'
}

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        
        # Balance
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo'),
                    html.H5('R$ 5400', id='p-balance-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-usd', style=card_icon),
                    color='info',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        
        # Revenue
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Receita'),
                    html.H5('R$ 10000', id='p-revenue-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-arrow-up', style=card_icon),
                    color='success',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        
        # Expense
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Despesa'),
                    html.H5('R$ 4600', id='p-expense-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-arrow-down', style=card_icon),
                    color='danger',
                    style={'maxWidth': 75, 'height': 100, 'margin-left': '-10px'}
                )
            ])
        ], width=4)
    ], style={'margin': '10px'}),
    
    dbc.Row([
        
        # Input filters
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar lançamentos', className='card-title'),
                html.Label('Categorias das receitas'),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-revenue',
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type='session',
                        multi=True
                    )
                ),
                
                html.Label(
                    'Categorias das despesas',
                    style={'margin-top': '10px'}
                ),
                
                dcc.Dropdown(
                    id='dropdown-expense',
                    clearable=False,
                    style={'width': '100%'},
                    persistence=True,
                    persistence_type='session',
                    multi=True
                ),
                
                html.Legend(
                    'Período de análise',
                    style={'margin-top': '10px'}
                ),
                
                dcc.DatePickerRange(
                    month_format='Do MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime(2022, 4, 1).date(),
                    end_date=datetime.today() + timedelta(days=31),
                    updatemode='singledate',
                    id='date-picker-config',
                    style={'z-index': '100'}
                )
            ], style={'height': '100%', 'padding': '20px'})
        ], width=4),
        
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='graph1'),
                style={'height': '100%', 'padding': '10px'}
            ), width=8 
        )
        
    ], style={'margin': '10px'})
])

# =========  Callbacks  =========== #

# Revenue filter + update revenue balance
@app.callback(
    [
        Output('dropdown-revenue', 'options'),
        Output('dropdown-revenue', 'value'),
        Output('p-revenue-dashboards', 'children')
    ],
    
    Input('store-revenue', 'data')
)
def populate_dropdown_values(data):
    df = pd.DataFrame(data)
    value = df['Valor'].sum()
    val = df.Categoria.unique().tolist()
    
    return ([{'label': x, 'value': x} for x in val], val, f'R$ {value}')

# Expense filter + update expense balance
@app.callback(
    [
        Output('dropdown-expense', 'options'),
        Output('dropdown-expense', 'value'),
        Output('p-expense-dashboards', 'children')
    ],
    
    Input('store-expense', 'data')
)
def populate_dropdown_values(data):
    df = pd.DataFrame(data)
    value = df['Valor'].sum()
    val = df.Categoria.unique().tolist()
    
    return ([{'label': x, 'value': x} for x in val], val, f'R$ {value}')

# Update total balance
@app.callback(
    Output('p-balance-dashboards', 'children'),
    
    [
        Input('store-revenue', 'data'),
        Input('store-expense', 'data')
    ]
)
def total_balance(revenue, expense):
    df_revenue = pd.DataFrame(revenue)
    df_expense = pd.DataFrame(expense)
    value = df_revenue['Valor'].sum() - df_expense['Valor'].sum()
    
    return f'R$ {value}'

# Update graph
@app.callback(
    Output('graph1', 'figure'),
    
    [
        Input('store-revenue', 'data'),
        Input('store-expense', 'data'),
        Input('dropdown-revenue', 'value'),
        Input('dropdown-expense', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date')
    ]
)
def graph_show(data_revenue, data_expense, revenue, expense, start_date, end_date):
    df_revenue = pd.DataFrame(data_revenue)
    df_expense = pd.DataFrame(data_expense)
    
    df_revenue['Output'] = 'Receitas'
    df_expense['Output'] = 'Despesas'
    df_final = pd.concat([df_revenue, df_expense])
    df_final['Data'] = pd.to_datetime(df_final['Data'])
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_final = df_final[(df_final['Data'] >= start_date) & (df_final['Data'] <= end_date)]
    df_final = df_final[(df_final['Categoria'].isin(revenue)) | (df_final['Categoria'].isin(expense))]
    
    fig = px.bar(
        df_final, 
        x='Data', 
        y='Valor', 
        color='Output', 
        barmode='group', 
        labels={'Output': ''}
    )
    
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=0), height=400)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig
    