from datetime import date as dt
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

# create app layout (main_container)
app.layout = html.Div(
    id='main-container',
    style={'backgroundColor': '#ffffff','display': 'inline-block'},
    children=[

        # define the left elements
        html.Div(
            className='four columns div-user-controls',
            id='left',
            style={'display': 'inline-block','height':'100%','verticalAlign':'middle','top':'0px','left':'0px'},
            children=[

                html.Div(
                    id='title',
                    style={'padding': 10,'backgroundColor': '#F9F9F9'},
                    children=[

                            html.H1(
                                children='Garmin Connect Dashboard',
                                style={'textAlign': 'center','color': '#7FDBFF'}
                            ),

                            html.P(
                                children='This dashboard allows users to view and analyse their excerise trends.',
                                style={'textAlign': 'center','color': '#779ECB'}
                            )
                        ]
                ),

                html.Div(
                    children=[

                        html.Div(
                            id='date',
                            style={'padding': 10,'textAlign': 'center','backgroundColor': '#F9F9F9'},
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
                            ]
                        )
                    ]
                ),
                html.Div(
                    id='image',
                    style={'padding': 10,'backgroundColor': '#F9F9F9'},
                    children = [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                                "align":"left"
                            },
                        )
                    ]
                )
            ]
        ),

        # define the right elements
        html.Div(
            className='eight columns div-for-charts bg-grey',
            id='right',
            style={'backgroundColor': '#F9F9F9','display': 'inline-block'}
        )

    ]
)


@app.callback(
    Output(component_id='right', component_property='children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_right(start_date, end_date):
    children = []

    #  ------- calculate KPIs
    # number of days in selected range
    n_days = (datetime.strptime(end_date,'%Y-%m-%d') - datetime.strptime(start_date,'%Y-%m-%d')).days
    
    # number of activities in selected range
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    n_activities = df2.activityId.nunique()

    # average duration of activity
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_dur = df2.duration.mean()

    # average calories
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_cal = df2.calories.mean()

    # average distance
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_dist = df2.distance.div(1000).mean()

    # average heart rate
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    avg_hr = df2.averageHR.mean()

    # add kpi div to children of "right" parent
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
    
    # add figures to "right" parent
    mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
    df2 = df.loc[mask]
    children.append(dcc.Graph(figure=make_bar_chart(df2), id='bar'))
    children.append(dcc.Graph(figure=make_scatter_plot(df2), id='scatter'))

    return children


###### call backs ######
# # text kpi callbacks
# @app.callback(
#     Output(component_id='kpis', component_property='children'),
#     [Input('my-date-picker-range', 'start_date'),
#      Input('my-date-picker-range', 'end_date')]
# )
# def display_kpis(start_date, end_date):
#     # number of days in selected range
#     n_days = (datetime.strptime(end_date,'%Y-%m-%d') - datetime.strptime(start_date,'%Y-%m-%d')).days
    
#     # number of activities in selected range
#     mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
#     df2 = df.loc[mask]
#     n_activities = df2.activityId.nunique()

#     # average duration of activity
#     mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
#     df2 = df.loc[mask]
#     avg_dur = df2.duration.mean()

#     # average calories
#     mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
#     df2 = df.loc[mask]
#     avg_cal = df2.calories.mean()

#     # average distance
#     mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
#     df2 = df.loc[mask]
#     avg_dist = df2.distance.div(1000).mean()

#     # average heart rate
#     mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
#     df2 = df.loc[mask]
#     avg_hr = df2.averageHR.mean()

#     # populate html elements with KPI values
#     kpis=[
#             html.Div(
#                 [html.P("Number of Days"),html.H6(n_days)],
#                 id="days",
#                 style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
#             ),
#             html.Div(
#                 [html.P("Number of Activities"),html.H6(n_activities)],
#                 id="activities",
#                 style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
#             ),
#             html.Div(
#                 [html.P("Avg Duration of Activities"),html.H6(f'{avg_dur:.2f} minutes')],
#                 id="duration",
#                 style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
#             ),
#             html.Div(
#                 [html.P("Avg Calories Burnt"),html.H6(f'{avg_cal:.2f}')],
#                 id="calories",
#                 style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
#             )
#             ,
#             html.Div(
#                 [html.P("Avg Distance"),html.H6(f'{avg_dist:.2f} km')],
#                 id="distance",
#                 style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
#             ),
#             html.Div(
#                 [html.P("Avg Heart Rate"),html.H6(f'{avg_hr:.2f} beats/min')],
#                 id="heart_rate",
#                 style={'padding': 10,'textAlign': 'center','color': "#779ECB"}
#             )
#         ]

#     return kpis


# @app.callback(
#     Output(component_id='figures', component_property='children'),
#     [Input('my-date-picker-range', 'start_date'),
#      Input('my-date-picker-range', 'end_date')]
# )
# def update_figures(start_date, end_date):
#     mask = (df['startTimeLocal'] > start_date) & (df['startTimeLocal'] <= end_date)
#     df2 = df.loc[mask]
#     # figures
#     figures = [
#         dcc.Graph(figure=make_bar_chart(df2), id='bar'),
#         dcc.Graph(figure=make_scatter_plot(df2), id='scatter')
#     ]

#     return figures


if __name__ == '__main__':
    app.run_server(debug=True)
