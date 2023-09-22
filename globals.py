import pandas as pd
import os

if ('df_revenue.csv' in os.listdir()) and ('df_expense.csv' in os.listdir()):
    df_revenue = pd.read_csv('df_revenue.csv', index_col=0, parse_dates=True)
    df_expense = pd.read_csv('df_expense.csv', index_col=0, parse_dates=True)
    
    df_revenue['Data'] = pd.to_datetime(df_revenue['Data'])
    df_expense['Data'] = pd.to_datetime(df_expense['Data'])
    df_revenue['Data'] = df_revenue['Data'].apply(lambda x: x.date())
    df_expense['Data'] = df_expense['Data'].apply(lambda x: x.date())
else:
    data_structure = {
        'Valor': [],
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descrição': []
    }
    df_revenue = pd.DataFrame(data_structure)
    df_expense = pd.DataFrame(data_structure)
    df_revenue.to_csv('df_revenue.csv')
    df_expense.to_csv('df_expense.csv')
    
if ('df_cat_revenue.csv' in os.listdir()) and ('df_cat_expense.csv' in os.listdir()):
    df_cat_revenue = pd.read_csv('df_cat_revenue.csv', index_col=0, parse_dates=True)
    df_cat_expense = pd.read_csv('df_cat_expense.csv', index_col=0, parse_dates=True)
    
    cat_revenue = df_cat_revenue.values.tolist()
    cat_expense = df_cat_expense.values.tolist()
else:
    cat_revenue = {'Categoria': ['Salário', 'Investimentos', 'Etc']}
    cat_expense = {'Categoria': ['Alimentação', 'Locomoção', 'Saúde', 'Lazer']}
    
    df_cat_revenue = pd.DataFrame(cat_revenue)
    df_cat_expense = pd.DataFrame(cat_expense)
    df_cat_revenue.to_csv('df_cat_revenue.csv')
    df_cat_expense.to_csv('df_cat_expense.csv')