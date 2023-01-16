# Import necessary libraries 
import dash
from dash import html
import dash_bootstrap_components as dbc

### Add the page components here 
# Define the final page layout
layout = dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("Show File Content", id="display-file-content-btn", color="success", style={'padding':'1em','width':'100%'}),
                    html.Div(children="File output will display here... ",id="display-file-content-response")
                ],
                style={'padding':'1em'})
            )
        ],style={'padding':'0.5em'}),
])