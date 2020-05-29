import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from garmin import get_garmin_data
from app import app, user1
import pandas as pd

# login layout
layout = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Location(id='url_login', refresh=True),
                html.Div('''Please log in to continue:''', id='h1'),
                html.Div(
                    # method='Post',
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            type='text',
                            id='uname-box'
                        ),
                        dcc.Input(
                            placeholder='Enter your password',
                            type='password',
                            id='pwd-box'
                        ),
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            type='submit',
                            id='login-button'
                        ),
                        html.Div(children='', id='output-state')
                    ]
                ),
            ]
        )
    ]
)

# first login callback - success or pass
@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, username, password):
    garmin = ["Success",pd.read_csv('data.csv')]
    #garmin = get_garmin_data(username,password)
    if garmin[0] == "Success":
        data = garmin[1]
        user1.update_username(username)
        user1.update_password(password)
        user1.update_data(data)
        user1.update_status(True)
        return '/home'
    else:
        pass 


# second login callback - unsuccessful logins
@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, username, password):
    if n_clicks > 0:
        #garmin = get_garmin_data(username,password)
        garmin = ["Success",pd.read_csv('data.csv')]
        if garmin[0] == "Success":
            data = garmin[1]
            user1.update_username(username)
            user1.update_password(password)
            user1.update_data(data)
            user1.update_status(True)
            return ''
        else:
            return garmin[0]
    else:
        ''
