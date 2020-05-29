# app
import dash
from user import User
from dash_bootstrap_components.themes import BOOTSTRAP

# user to be updated on login and used in success view
user1 = User(None,None,None,False)

app = dash.Dash(__name__,
                external_stylesheets=[BOOTSTRAP],
                suppress_callback_exceptions=True)

server = app.server
