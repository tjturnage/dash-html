from datetime import datetime
import numpy as np


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

now = datetime.utcnow()
endyear = now.year + 1
root_dir = 'C:/data/'
#root_dir = '/home/tjturnage/'
DATA_DIR = root_dir + 'TEXT_DATA'
FSW_OUT_DATA = os.path.join(root_dir,'FSW_OUTPUT/fsw_output.txt')
print(FSW_OUT_DATA)

def build_range_slider():
    year_list = list(np.arange(1996,endyear,1))
    years_str = [str(x) for x in year_list]
    marks = [str(x)[-2:] for x in year_list]
    marks_dict = dict(zip(years_str, marks))
    return marks_dict

def create_dataframe():
    dts = []
    product = []
    with open(FSW_OUT_DATA,'r') as src:
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

df = create_dataframe()

app.layout = dbc.Container([

            html.Div(
                dcc.Textarea(
                    id='word-list',
                    value='Enter List Here',
                    style={'width': '100%', 'height': 300},
                ),
            align="center"
        ),
            dbc.Row(
            [
                dbc.Col(html.H3('Word Search Method'), md=6),
                dbc.Col(html.H3('Search Selection Method'), md=6),
            ],
            align="center"
        ),
                dbc.Row(
            [
                dbc.Col(dcc.RadioItems(id='word-search',options=['All words','Any words'],value='Any words'), md=6),
                dbc.Col(dcc.RadioItems(id='selection-search',options=['By Forecast','By Day'],value='By Forecast'), md=6),
            ],
            align="center"
        ),
            html.Div(
            [   html.H2(children="Select Range of Years to Search"),
                dcc.RangeSlider(min=1996,max=endyear,step=None,marks=build_range_slider(),value=['2000','2015'],allowCross=False),
            ],
        )], style={'border-color':'blue'}
            ),
            dbc.Row(
            [
                dbc.Col(html.H2('Select Product and Station to be Plotted Below'), md=12),
            ],
            align="center"
        ),
            dbc.Row(
            [
                dbc.Col(dcc.RadioItems(id='product-picker',options=product_options,value='AFD'), md=4),
                dbc.Col(dcc.RadioItems(id='wfo-picker',options=wfo_options,value='GRR'), md=4),
            ],
            align="center"
        ),
            html.Div(
            [dcc.Graph(id='trend')]
            ),
    
    
@app.callback(Output('trend', 'figure'),
              [Input('product-picker', 'value'),
              Input('wfo-picker', 'value')
              ])

def update_figure(product, wfo):
    tracename = f'Frequency of "Lake Effect" mentioned in {product} issued from {wfo}'
    fullname = f'{product}{wfo}'
    filtered = df[df['product'] == fullname]
    monthly = filtered.resample('M').count()
    trace = [go.Scatter(
            x=monthly.index,
            y=monthly['product'],
            name=tracename
            )]

    return {
        'data':trace,
        'layout': go.Layout(
                xaxis={'title':'Month'},
                yaxis={'title':'Frequency'},
                hovermode='closest',
                title=tracename
            )}

if __name__ == '__main__':
    app.run_server()