from datetime import date as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from garmin import get_garmin_data
from config import EMAIL,PASSWORD
from figures import make_bar_chart, make_scatter_plot


###### bring in garmin data ######
#df = get_garmin_data(EMAIL,PASSWORD)
df = pd.read_csv('data.csv')

###### figures ######
bar = make_bar_chart(df)
sca = make_scatter_plot(df)

###### initialize app ######
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# create app layout
app.layout = html.Div(
    children=[

        # define the left elements
        html.Div(
            children=[

                html.Div(
                    children=[

                            html.H1(
                                children='Garmin Connect Dashboard',
                                style={'textAlign': 'center','color': '#7FDBFF'}
                            ),

                            html.P(
                                children='This dashboard allows users to view and analyse their excerise trends.',
                                style={'textAlign': 'center','color': '#779ECB'}
                            )
                        ],
                        id='title',
                ),

                html.Div(
                    children=[

                        html.Div(
                            children=[
                                html.P('Select Dates Below',
                                    style={'textAlign': 'center','color': "#779ECB"}
                                ),
                                dcc.DatePickerRange(
                                    id='my-date-picker-range',
                                    month_format='MMM Do, YY',
                                    start_date=df.startTimeLocal.min(),
                                    end_date=df.startTimeLocal.max(),
                                    end_date_placeholder_text="End Date",
                                    min_date_allowed=df.startTimeLocal.min(),
                                    max_date_allowed=dt.today()
                                ),
                                html.Div(id='output-container-date-picker-range'
                                )
                            ],
                            id='date',
                            style={'padding': 10,'textAlign': 'center'}
                        )
                    ]
                ),
                html.Div(
                    html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                                "align":"left"
                            },
                    ),
                    id='image'
                )
            ],
            className='four columns div-user-controls',
            id='left',
            style={'backgroundColor': '#F9F9F9'}
        ),

        # define the right elements
        html.Div(
            children=[

                dcc.Graph(figure=bar,id='bar'),
                dcc.Graph(figure=sca,id='scatter')
            ],
            className='eight columns div-for-charts bg-grey',
            id='right',
            style={'backgroundColor': '#F9F9F9'}
        )

    ],
    id='main-container',
    style={'backgroundColor': '#F9F9F9'}
)

# call backs
@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)

def update_bar(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    bar2 = make_bar_chart(df2)
    return bar2

###### call backs ######
@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)

def update_scatetr(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    sca2 = make_scatter_plot(df2)
    return sca2

if __name__ == '__main__':
    app.run_server(debug=True)
