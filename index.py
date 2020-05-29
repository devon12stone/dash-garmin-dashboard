# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, user1
# can only instantiate home in if statement in order to not get null error
from views import login


header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%','width': '100%', 'display': 'inline-block'},
        children=[
            html.Img(
                src='assets/dash-logo-stripe.svg',
                className='logo',
                style = {'vertical-align': 'middle','float':'left'}
            ),
            html.H1(
                'Garmin Connect Dashboard',
                style={'color': '#506784', 'vertical-align': 'middle', 'float':'right', 'margin-top': '5px'}
            )
        ]
    )
)

app.layout = html.Div(
    [   
        dcc.Location(id='url', refresh=False),
        header,
        html.Div(id='page-content', className='content',style={'height': '100%','width': '100%'})
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname == '/':
        if user1.status:
            from views import home
            return home.layout
        else:
            return login.layout

    elif pathname == '/home':
        if user1.status:
            from views import home
            return home.layout
        else:
            return login.layout
            
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
