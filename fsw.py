#from datetime import datetime
#import numpy as np

import re
from textwrap import wrap
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import glob
import os

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'])


root_dir = '/data/'
root_dir = '/home/tjturnage/'
DATA_DIR = root_dir + 'TEXT_DATA'
FSW_OUT_DATA = root_dir + 'FSW_OUT/fsw_out.txt'

def create_dataframe():
    dts = []
    product = []
    with open('FSW_OUT_DATA','r') as src:
        for line in src.readlines():
            if line[0] in ('0','1'):
                values = line.split('\t')
                dts.append(values[0])
                product.append(values[1][1:])

    #print(dts,product)
    dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
    data = {'dts':dts_pd, 'product':product}
    df = pd.DataFrame(data)
    df.set_index('dts', inplace=True)
    return df

def get_master_list():
    os.chdir(DATA_DIR)
    master = glob.glob('*',recursive=True)
    return master

def specific_products_directories():
    wfo_options = []
    product_options = []
    for i in master_list:
        if len(i) == 6:
            product = i[:3]
            stn = i[-3:]
            if stn not in wfo_options:
                wfo_options.append(stn)
            if product not in product_options:
                product_options.append(product)
        else:
            pass
    
    #print(product_options, wfo_options)
    return product_options, wfo_options

master_list = get_master_list()

product_options, wfo_options = specific_products_directories()
#afd_options = specific_products_directories('AFD')
df = create_dataframe()

app.layout = dbc.Container(
    [

        dbc.Row(
            [
                dbc.Col(html.H2(["Select the products and issuing sites to analyze"]), md=12),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.H4([""]), md=2),
                dbc.Col(html.H4(["Product"]), md=2),
                dbc.Col(html.H4(["Site"]), md=2),
                dbc.Col(html.H4([""]), md=2),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.H4([""]), md=2),
                dbc.Col(dcc.Checklist(id='product-picker',options=product_options,value='AFD'), md=2),
                dbc.Col(dcc.Checklist(id='wfo-picker',options=wfo_options,value='GRR'), md=2),
                dbc.Col(html.H4([""]), md=2),
            ],
            align="center",
        ),
        dcc.Graph(id='trend',
        figure={
            'data':[go.Scatter(
                x=df.index,
                y=df['product'],
                text=df['product'],
                hoverinfo='text',
                mode='markers'
            )]
        })
        ],
        align="center",
        ),

#fluid=True,

@app.callback(Output('graph', 'figure'),
              [Input('product-picker', 'value'),
              Input('wfo-picker', 'value')
              ])
def update_figure(selected_year, element):
    tracename = f'Grand Rapids {element[:-2]} Departures from Normal for {selected_year}'
    filtered_df = df[df.index.year == selected_year]
    trace = [go.Heatmap(
            x=filtered_df['month'],
            y=filtered_df['day'],
            z=filtered_df[element],colorscale='RdBu',reversescale=True,zmin=-25,zmax=25,
            name=tracename
            )]

    return {
        'data':trace,
        'layout': go.Layout(
                xaxis={'title':'Month'},
                yaxis={'title':'Day of Month'},
                hovermode='closest',
                title=tracename
            )}

if __name__ == '__main__':
    app.run_server()