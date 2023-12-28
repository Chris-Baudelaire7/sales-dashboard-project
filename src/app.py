import dash
from flask import Flask
from dash import html
from dash_extensions.enrich import DashProxy
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from apps import navbar
from callbacks import *


# Parameters 

app_params = {
    "server": Flask(__name__),
    "title": "Sales Dashboard Analysis",
    "use_pages": True,
    "url_base_pathname": "/",
    "external_stylesheets": [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    "suppress_callback_exceptions": True,
    "prevent_initial_callbacks": True,
    "meta_tags": [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
}

server_params = {"debug": True}


# Create app

app = DashProxy(__name__, **app_params)  # or Dash(__name__, **app_params) 

server = app.server

app.layout = dmc.NotificationsProvider(
    html.Div(id="app", children=[
        
        html.Div(id="notifications-container"),
    
        navbar.navbar, 
            
        dash.page_container
        
    ]),
    transitionDuration=4000
)


# Launch server app

if __name__ == '__main__':
    app.run_server(**server_params)