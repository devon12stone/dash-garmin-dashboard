from datetime import date as dt
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
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
                dbc.Row(
                    children=[
                        html.Div(
                            [html.P("Number of Days"),html.H6(id="days_text")],
                            id="days",
                            style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                        ),
                        html.Div(
                            [html.P("Number of Activities"),html.H6(id="activities_text")],
                            id="activities",
                            style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                        )

                    ],
                    id='kpi_days',
                    align="center"
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

###### call backs ######
# text kpi callbacks
@app.callback(
    dash.dependencies.Output('days_text', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_days_text(start_date, end_date):
    days = (datetime.strptime(end_date,'%Y-%m-%d') - datetime.strptime(start_date,'%Y-%m-%d')).days
    return days

@app.callback(
    dash.dependencies.Output('activities_text', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_activities_text(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    no_activities = df2.activityId.nunique()
    return no_activities


# figure callbacks
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
