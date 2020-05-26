# app
import dash
from user import User
from dash_bootstrap_components.themes import BOOTSTRAP

app = dash.Dash(__name__, external_stylesheets=[BOOTSTRAP], suppress_callback_exceptions=True)

# user to be updated on login and used in success view
user1 = User(None, None, None)

