import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import date, datetime
import plotly.express as px
import numpy as no
import pandas as pd

from globals import *

sb_style = {
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px'
}

# ========= Layout ========= #
layout = dbc.Col([
    html.Img(
        src='/assets/logoapp.png',
        className='logo_app',
        style={'margin-left': '10px'}
    ),
    
    # Add revenue/expense buttons
    dbc.Row([
        dbc.Col([
            dbc.Button(
                color='success', 
                id='open-new-revenue',
                children=['Receita']
            )
        ], width=6),
        dbc.Col([
            dbc.Button(
                color='danger', 
                id='open-new-expense',
                children=['Despesa']
            )
        ], width=6)
    ], style={'margin-top': '25px', 'margin-bottom': '25px'}),
    
    # Modal + revenue
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição da receita: '),
                    dbc.Input(placeholder="Ex.: salário, dividendos...", id='revenue-txt')
                ], width=6, style={'margin-right': '63px'}),
                
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder="R$100.00", id='revenue-value', value='')
                ], width=5)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(
                        id='revenue-date',
                        min_date_allowed=date(2020, 1, 1),
                        max_date_allowed=date(2030, 12, 31),
                        date=datetime.today(),
                        style={'width': '100%'}
                    )
                ], width=4),
                
                dbc.Col([
                    dbc.Label('Extras'),
                    dbc.Checklist(
                        options=[
                            {'label': 'Recebida', 'value': 1},
                            {'label': 'Recorrente', 'value': 2}
                        ],
                        value=[1],
                        id='switches-input-revenue',
                        switch=True
                    )
                ], width=4),
                
                dbc.Col([
                    html.Label('Categoria da receita'),
                    dbc.Select(
                        id='select-revenue',
                        options=[{'label': i, 'value': i} for i in cat_revenue],
                        value=cat_revenue[0]
                    )
                ], width=4)
            ], style={'margin-top': '25px'}),
            
            # Add/remove category
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend(
                                        'Adicionar categoria'
                                    ),
                                    dbc.Input(
                                        type='text',
                                        placeholder='Nova categoria',
                                        id='input-add-revenue',
                                        value=''
                                    ),
                                    html.Br(),
                                    dbc.Button(
                                        'Adicionar', 
                                        className='btn btn-success',
                                        id='add-category-revenue',
                                        style={"margin-top": '20px'}
                                    ),
                                    html.Br(),
                                    html.Div(
                                        id='category-div-add-revenue',
                                        style={}
                                    )
                                ], width=6),
                                
                                dbc.Col([
                                    html.Legend(
                                        'Remover categoria'
                                    ),
                                    dbc.Checklist(
                                        id='checklist-selected-style-revenue',
                                        options=[{'label': i, 'value': i} for i in cat_revenue],
                                        value=[],
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={'backgroundColor': 'blue', 'borderColor': 'red'}
                                    ),
                                    dbc.Button(
                                        'Remover',
                                        color='danger',
                                        id='remove-category-revenue',
                                        style={'margin-top': '20px'}
                                    )
                                ], width=5, style={'margin-left': '30px'})
                            ])
                        ], title='Adicionar ou remover categorias')
                ], flush=True, start_collapsed=True, id='accordion-revenue'),
                
                html.Div(
                    id='id-revenue-test',
                    style={'padding-top': '20px'},
                ),
                dbc.ModalFooter([
                    dbc.Button(
                        'Adicionar receita',
                        id='save-revenue',
                        color='success'
                    ),
                    
                    dbc.Popover(
                        dbc.PopoverBody('Receita salva'),
                        target='save-revenue',
                        placement='left',
                        trigger='click'
                    )
                ])
            ], style={'margin-top': '25px'})
        ])
    ], 
    style={'background-color': 'rgba(17, 140, 79, 0.05)'},
    id='new-revenue-modal',
    size='lg',
    is_open=False,
    centered=True,
    backdrop=True
    ),
    
    # Modal - expense
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição da despesa: '),
                    dbc.Input(placeholder="Ex.: gasolina, supermercado...", id='expense-txt')
                ], width=6, style={'margin-right': '63px'}),
                
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder="R$100.00", id='expense-value', value='')
                ], width=5)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(
                        id='expense-date',
                        min_date_allowed=date(2020, 1, 1),
                        max_date_allowed=date(2030, 12, 31),
                        date=datetime.today(),
                        style={'width': '100%'}
                    )
                ], width=4),
                
                dbc.Col([
                    dbc.Label('Extras'),
                    dbc.Checklist(
                        options=[
                            {'label': 'Pago', 'value': 1},
                            {'label': 'Recorrente', 'value': 2}
                        ],
                        value=[1],
                        id='switches-input-expense',
                        switch=True
                    )
                ], width=4),
                
                dbc.Col([
                    html.Label('Categoria da despesa'),
                    dbc.Select(
                        id='select-expense',
                        options=[{'label': i, 'value': i} for i in cat_expense],
                        value=cat_expense[0]
                    )
                ], width=4)
            ], style={'margin-top': '25px'}),
            
            # Add/remove category
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend(
                                        'Adicionar categoria'
                                    ),
                                    dbc.Input(
                                        type='text',
                                        placeholder='Nova categoria',
                                        id='input-add-expense',
                                        value=''
                                    ),
                                    html.Br(),
                                    dbc.Button(
                                        'Adicionar', 
                                        className='btn btn-success',
                                        id='add-category-expense',
                                        style={"margin-top": '20px'}
                                    ),
                                    html.Br(),
                                    html.Div(
                                        id='category-div-add-expense',
                                        style={}
                                    )
                                ], width=6),
                                
                                dbc.Col([
                                    html.Legend(
                                        'Remover categoria'
                                    ),
                                    dbc.Checklist(
                                        id='checklist-selected-style-expense',
                                        options=[{'label': i, 'value': i} for i in cat_expense],
                                        value=[],
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={'backgroundColor': 'blue', 'borderColor': 'red'}
                                    ),
                                    dbc.Button(
                                        'Remover',
                                        color='danger',
                                        id='remove-category-expense',
                                        style={'margin-top': '20px'}
                                    )
                                ], width=5, style={'margin-left': '30px'})
                            ])
                        ], title='Adicionar ou remover categorias')
                ], flush=True, start_collapsed=True, id='accordion-expense'),
                
                html.Div(
                    id='id-expense-test',
                    style={'padding-top': '20px'},
                ),
                dbc.ModalFooter([
                    dbc.Button(
                        'Adicionar despesa',
                        id='save-expense',
                        color='danger'
                    ),
                    
                    dbc.Popover(
                        dbc.PopoverBody('Despesa salva'),
                        target='save-expense',
                        placement='left',
                        trigger='click'
                    )
                ])
            ], style={'margin-top': '25px'})
        ])
    ], 
    style={'background-color': 'rgba(17, 140, 79, 0.05)'},
    id='new-expense-modal',
    size='lg',
    is_open=False,
    centered=True,
    backdrop=True
    ),
    
    html.Hr(), # Line break
    
    # Navigation
    dbc.Nav([
        dbc.NavLink('Dashboard', href="/dashboards", active='exact'),
        dbc.NavLink('Extratos', href="/extratos", active='exact')
    ], vertical=True, pills=True, id='nav_buttons', style={'margin-bottom': '50px'})

], id='full_sidebar', style=sb_style)

# ========= Callbacks ========= #

# Revenue pop-up
@app.callback(
    Output('new-revenue-modal', 'is_open'),
    Input('open-new-revenue', 'n_clicks'),
    State('new-revenue-modal', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Expense pop-up
@app.callback(
    Output('new-expense-modal', 'is_open'),
    Input('open-new-expense', 'n_clicks'),
    State('new-expense-modal', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# New revenue
@app.callback(
    Output('store-revenue', 'data'),
    Input('save-revenue', 'n_clicks'),
    [
        State('revenue-txt', 'value'),
        State('revenue-value', 'value'),
        State('revenue-date', 'date'),
        State('switches-input-revenue', 'value'),
        State('select-revenue', 'value'),
        State('store-revenue', 'data'),
    ]
)
def save_form_revenue(n, description, value, date, switches, category, dict_revenue):
    df_revenue = pd.DataFrame(dict_revenue)
    
    if n and not (value == '' or value == None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category
        received = 1 if 1 in switches else 0
        recurrent = 1 if 2 in switches else 0
        
        df_revenue.loc[df_revenue.shape[0]] = [value, received, recurrent, date, category, description]
        df_revenue.to_csv('df_revenue.csv')
    
    data_return = df_revenue.to_dict()
    return data_return

# New expense
@app.callback(
    Output('store-expense', 'data'),
    Input('save-expense', 'n_clicks'),
    [
        State('expense-txt', 'value'),
        State('expense-value', 'value'),
        State('expense-date', 'date'),
        State('switches-input-expense', 'value'),
        State('select-expense', 'value'),
        State('store-expense', 'data'),
    ]
)
def save_form_expense(n, description, value, date, switches, category, dict_expense):
    df_expense = pd.DataFrame(dict_expense)
    
    if n and not (value == '' or value == None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category
        paid = 1 if 1 in switches else 0
        recurrent = 1 if 2 in switches else 0
        
        df_expense.loc[df_expense.shape[0]] = [value, paid, recurrent, date, category, description]
        df_expense.to_csv('df_expense.csv')
    
    data_return = df_expense.to_dict()
    return data_return

# Add/remove revenue
@app.callback(
    [
        Output('select-revenue', 'options'),
        Output('checklist-selected-style-revenue', 'options'),
        Output('checklist-selected-style-revenue', 'value'),
        Output('store-cat-revenue', 'data'),
    ],
    
    [
        Input('add-category-revenue', 'n_clicks'),
        Input('remove-category-revenue' ,'n_clicks')
    ],
    
    [
        State('input-add-revenue', 'value'),
        State('checklist-selected-style-revenue', 'value'),
        State('store-cat-revenue', 'data')
    ]
)
def add_remove_category(n, n2, txt, check_delete, data):
    cat_revenue = list(data['Categoria'].values())
    
    if n and not (txt == '' or txt == None):
        cat_revenue = cat_revenue + [txt] if txt not in cat_revenue else cat_revenue
    if n2:
        if len(check_delete) > 0:
            cat_revenue = [i for i in cat_revenue if i not in check_delete]
    
    opt_revenue = [{'label': i, 'value': i} for i in cat_revenue]
    df_cat_revenue = pd.DataFrame(cat_revenue, columns=['Categoria'])
    df_cat_revenue.to_csv('df_cat_revenue.csv')
    data_return = df_cat_revenue.to_dict()
    
    return [opt_revenue, opt_revenue, [], data_return]

# Add/remove expense
@app.callback(
    [
        Output('select-expense', 'options'),
        Output('checklist-selected-style-expense', 'options'),
        Output('checklist-selected-style-expense', 'value'),
        Output('store-cat-expense', 'data'),
    ],
    
    [
        Input('add-category-expense', 'n_clicks'),
        Input('remove-category-expense' ,'n_clicks')
    ],
    
    [
        State('input-add-expense', 'value'),
        State('checklist-selected-style-expense', 'value'),
        State('store-cat-expense', 'data')
    ]
)
def add_remove_category(n, n2, txt, check_delete, data):
    cat_expense = list(data['Categoria'].values())
    
    if n and not (txt == '' or txt == None):
        cat_expense = cat_expense + [txt] if txt not in cat_expense else cat_expense
    if n2:
        if len(check_delete) > 0:
            cat_expense = [i for i in cat_expense if i not in check_delete]
    
    opt_expense = [{'label': i, 'value': i} for i in cat_expense]
    df_cat_expense = pd.DataFrame(cat_expense, columns=['Categoria'])
    df_cat_expense.to_csv('df_cat_expense.csv')
    data_return = df_cat_expense.to_dict()
    
    return [opt_expense, opt_expense, [], data_return]
