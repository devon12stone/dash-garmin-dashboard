from datetime import date as dt
from datetime import datetime
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
                        style={'padding': 10,'backgroundColor': '#F9F9F9'}
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
                            style={'padding': 10,'textAlign': 'center','backgroundColor': '#F9F9F9'}
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
                    id='image',
                    style={'padding': 10,'backgroundColor': '#F9F9F9'}
                )
            ],
            className='four columns div-user-controls',
            id='left',
            style={'display': 'inline-block','height':'100%','verticalAlign':'middle','top':'0px','left':'0px'}
        ),

        # define the right elements
        html.Div(
            children=[

                html.Div(
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
                        ),
                        html.Div(
                            [html.P("Avg Duration of Activities"),html.H6(id="duration_text")],
                            id="duration",
                            style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                        ),
                        html.Div(
                            [html.P("Avg Calories Burnt"),html.H6(id="cal_text")],
                            id="calories",
                            style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                        )
                        ,
                        html.Div(
                            [html.P("Avg Distance"),html.H6(id="dist_text")],
                            id="distance",
                            style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                        ),
                        html.Div(
                            [html.P("Avg Heart Rate"),html.H6(id="hr_text")],
                            id="heart_rate",
                            style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                        )

                    ],
                    id='kpi_days',
                    style={"display": "flex", "flex-direction": "row",'align': 'center','padding': 10}
                ),

                dcc.Graph(figure=make_bar_chart(df),id='bar'),
                dcc.Graph(figure=make_scatter_plot(df),id='scatter')
            ],
            className='eight columns div-for-charts bg-grey',
            id='right',
            style={'backgroundColor': '#F9F9F9','display': 'inline-block'}
        )

    ],
    id='main-container',
    style={'backgroundColor': '#ffffff','display': 'inline-block'}
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

@app.callback(
    dash.dependencies.Output('duration_text', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_duration_text(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_dur = round(df2.duration.mean(),2)
    avg_str = "{dur} minutes".format(dur=str(avg_dur))
    return avg_str

@app.callback(
    dash.dependencies.Output('cal_text', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_calories_text(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_cal = round(df2.calories.mean(),2)
    return avg_cal

@app.callback(
    dash.dependencies.Output('dist_text', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_distance_text(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_dist = round(df2.distance.div(1000).mean(),2)
    avg_str = "{d} km".format(d=str(avg_dist))
    return avg_str

@app.callback(
    dash.dependencies.Output('hr_text', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_distance_text(start_date, end_date):
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_hr = round(df2.averageHR.mean(),2)
    avg_str = "{hr} beats/min".format(hr=str(avg_hr))
    return avg_str

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
