# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("turnageweather", href="/home")),
                dbc.NavItem(dbc.NavLink("SPC graphics download", href="/spcdownload")),
                dbc.NavItem(dbc.NavLink("AFDs", href="/afds")),
            ] ,
            brand="turnageweather",
            brand_href="/home",
            color="dark",
            dark=True,
        ), 
    ])

    return layout
