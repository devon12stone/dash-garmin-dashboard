# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, user1
from views import login, home


header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src='assets/dash-logo-stripe.svg',
                className='logo'
            ),
            html.Div(className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ])
        ]
    )
)

app.layout = html.Div(
    [   
        dcc.Location(id='url', refresh=False),
        header,
        html.Div(id='page-content', className='content')
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # TODO: if user goes to / then it should either
    # go to login screen (if not logged in) or home
    if pathname == '/login':
        return login.layout
    # TODO: if user tries to navigate to home while
    # not logged in, it should send them to login
    elif pathname == '/home':
        return home.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
