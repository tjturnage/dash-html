# Import necessary libraries 
import dash
from dash import html
import dash_bootstrap_components as dbc

### Add the page components here 
# Define the final page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Welcome to turnageweather!")),
    ])
])