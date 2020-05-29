from datetime import date as dt
from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from garmin import get_garmin_data
from figures import make_bar_chart, make_scatter_plot
from app import app, user1

# logged-in user's data
df = user1.data

# create app layout (main_container)
layout = html.Div(
    [
        dcc.Store(id='store'),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label='Summary', tab_id='summary'),
                dbc.Tab(label='Calories', tab_id='calories'),
            ],
            id='tabs',
            active_tab='summary'
        ),
        # date selector
        html.Div(
            id='date-selector',
            className='p-4',
            style={'padding':0, 'textAlign':'center'},
            children=[
                html.P('Select Dates Below',
                    style={'padding':0, 'margin':0, 'textAlign':'center', 'color':"#779ECB"}
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
            ]
        ),
        html.Div(id='tab-content', className='p-4'),
    ]
)


@app.callback(
    Output(component_id='tab-content', component_property='children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('tabs', 'active_tab')]
)
def update_tab(start_date, end_date, active_tab):
    children = []
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]

    #  ------- calculate KPIs
    # number of days in selected range
    n_days = (datetime.strptime(end_date,'%Y-%m-%d') - datetime.strptime(start_date,'%Y-%m-%d')).days
    # number of activities in selected range
    n_activities = df2.activityId.nunique()
    # average duration of activity
    avg_dur = df2.duration.mean()
    # average calories
    avg_cal = df2.calories.mean()
    # average distance
    avg_dist = df2.distance.div(1000).mean()
    # average heart rate
    avg_hr = df2.averageHR.mean()

    # add kpi div to children of "tab-content" parent
    # TODO: make these KPIs specific to the tab selected
    # TODO: move the logic into a separate `tabs` subfolder?
    children.append(
        html.Div(
            id='kpi_days',
            style={"display": "flex", "flex-direction": "row",'align': 'center','padding': 10},
            children=[
                html.Div(
                    [html.P("Number of Days"),html.H6(n_days)],
                    id="days",
                    style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                ),
                html.Div(
                    [html.P("Number of Activities"),html.H6(n_activities)],
                    id="activities",
                    style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                ),
                html.Div(
                    [html.P("Avg Duration of Activities"),html.H6(f'{avg_dur:.2f} minutes')],
                    id="duration",
                    style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                ),
                html.Div(
                    [html.P("Avg Calories Burnt"),html.H6(f'{avg_cal:.2f}')],
                    id="calories",
                    style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                )
                ,
                html.Div(
                    [html.P("Avg Distance"),html.H6(f'{avg_dist:.2f} km')],
                    id="distance",
                    style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                ),
                html.Div(
                    [html.P("Avg Heart Rate"),html.H6(f'{avg_hr:.2f} bpm')],
                    id="heart_rate",
                    style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
                )
            ]
        )
    )
    
    # add selected figure to "tab-content" parent
    if active_tab == 'summary':
        children.append(dcc.Graph(figure=make_bar_chart(df2), id='bar'))
    elif active_tab == 'calories':
        children.append(dcc.Graph(figure=make_scatter_plot(df2), id='scatter'))

    return children
