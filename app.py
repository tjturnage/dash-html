# Define the Dash App and it's properties here 

import dash
from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Welcome to turnageweather!")),
    ])
])

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)