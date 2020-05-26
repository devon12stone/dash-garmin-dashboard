# app
import dash
from user import User

app = dash.Dash(__name__,suppress_callback_exceptions = True)

# user to be updated on login and used in success view
user1 = User(None,None,None)

