from datetime import datetime
import pandas as pd
import numpy as np
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from urllib.request import urlopen
import json
import json, requests
#from XAcis_class import XAcis


month_dict = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
                7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

month_dict_zero = {0:'January',1:'February',2:'March',3:'April',4:'May',5:'June',
                6:'July',7:'August',8:'September',9:'October',10:'November',11:'December'}

month_list = ['January','February','March','April','May','June','July',
              'August','September','October','November','December']


base_url = "http://data.rcc-acis.org/StnData?params="
stationid = ["kgrr"]
outdir = "C:/data/scripts/dash/"
# RCC ACIS url for the API. 


#timescale = {"dly":"1","mly":"2","yly":"3"}
timescale = ["dly"]

dfcolumns = ["dts","AvgT","MaxT","MaxT_d","MinT","MinT_d"]

def make_request(url,values): 
    req = requests.post(url,json=values)
    return req.json()

# Looping through the keys of the station_id and timescale.
for stations in stationid:
    for time in timescale:
# Creating the json query string to grab the normal data. See the rcc-acis.org
# Web Services documentation if creating another request. 
        inputdict = {
            "sid":stations,
            "sdate":"2010-01-01",
            "edate":"2022-07-07",
            "elems":[{"name":"avgt","interval":time,"duration":time,"normal":"1"},
            {"name":"maxt","interval":time,"duration":time},
            {"name":"maxt","interval":time,"duration":time,"normal":"departure"},
            {"name":"mint","interval":time,"duration":time},
            {"name":"mint","interval":time,"duration":time,"normal":"departure"}],
            #{"name":"pcpn","interval":time,"duration":time,"normal":"1"},
            #{"name":"snow","interval":time,"duration":time,"normal":"1"},
            #{"name":"hdd","interval":time,"duration":time,"normal":"1"},
            #{"name":"cdd","interval":time,"duration":time,"normal":"1"}],
        }
# Sending the data that comes back from RCC ACIS into a few pandas
        data = make_request(base_url,inputdict)
# This normalizes the initial json that is sent back.
        df_init = pd.json_normalize(data)
        df_dp = df_init["data"].apply(pd.Series).T
# Another formatting step to put the series of columns into another panda
# dataframe. Then the coulumn headers are added at the end.
        df = df_dp[0].apply(pd.Series)
        df.columns = dfcolumns
        df['date'] = pd.DatetimeIndex(df['dts'])
        df.set_index('date', inplace=True)
        df.drop('dts',axis=1,inplace=True)
        #df['value'] = df['value'].astype(int)
        df['month'] = [month_dict[m] for m in list(df.index.month)]
        df['day'] = [d for d in list(df.index.day)]
        print(df)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


# https://dash.plot.ly/dash-core-components/dropdown
# We need to construct a dictionary of dropdown values for the years
year_options = []
for year in df.index.year.unique():
    year_options.append({'label':str(year),'value':year})

app.layout = html.Div([
        dcc.Graph(id='graph'),
        html.Div([
            dcc.Slider(min=2010, max=2022,
                step=1,
                value=2010,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                id='year-picker'),
                html.Div(id='slider-output-container')
                ],
                style={'padding': '40px'}
                )
        ],
        style={'padding': '40px'})

@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])
def update_figure(selected_year):
    
    filtered_df = df[df.index.year == selected_year]
    trace = [go.Heatmap(
            x=filtered_df['month'],
            y=filtered_df['day'],
            z=filtered_df['MaxT_d'],colorscale='RdBu',reversescale=True,zmin=-25,zmax=25,
            name=f'Daily temps for {selected_year}'
            )]

    return {
        'data':trace,
        'layout': go.Layout(
                xaxis={'title':'Month'},
                yaxis={'title':'Day of Month'},
                hovermode='closest',
                title=f'GRR Max T Departures from Normal for {selected_year}'
            )}
             
"""
@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])
def update_figure(selected_year):
    
    filtered_df = df[df.index.year == selected_year]
    trace = [go.Violin(filtered_df, y="MaxT",
            x="month",
            name=f'Daily temps for {selected_year}'
            )]

    return {
        'data':trace,
        'layout': go.Layout(
                xaxis={'title':'Month'},
                #yaxis={'title':'MaxT'},
                hovermode='closest',
                title=f'GRR Max T Departures from Normal for {selected_year}'
            )}
            
"""

if __name__ == '__main__':
    app.run_server()