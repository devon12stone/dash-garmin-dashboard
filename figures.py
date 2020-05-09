import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


def make_bar_chart(df):
    # input: pandas df
    # output: plotly express bar chart

    bar_data = df['activityType'].value_counts()
    bar_data = bar_data.to_frame()
    bar_data = bar_data.rename(columns={"activityType": "Count", "B": "c"})
    bar_data['Activity Type'] = bar_data.index
    bar_data = bar_data.reset_index()

    bar = px.bar(bar_data,
                 x='Activity Type',
                 y='Count',
                 hover_data=['Activity Type', 'Count'],
                 color='Activity Type'
    )

    # remove activity type from legend
    for trace in bar.data:
        trace.name = trace.name.split('=')[1]

    bar.update_layout(
        title={'text':'Exercise Type Breakdown','y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'},
        plot_bgcolor='whitesmoke',
        font={'family':"Courier New, monospace",'size':10,'color':"#7f7f7f"},
        legend={'x': 0.75, 'y': 0.9, 'traceorder':'normal'}
    )

    return bar

def make_scatter_plot(df):
    # input: pandas df
    # output: plotly express scatter plot

    sca = px.scatter(df,
                     x='duration',
                     y='calories',
                     hover_data=['duration', 'calories'],
                     color='activityType'
    )

    # remove activity type from legend
    for trace in sca.data:
        trace.name = trace.name.split('=')[1]

    sca.update_traces(
        marker={'size':12}
    )

    sca.update_layout(
        title={'text':'Duration vs Calories Burnt','y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'},
        plot_bgcolor='whitesmoke',
        font={'family':"Courier New, monospace",'size':10,'color':"#7f7f7f"},
        legend={'x': 0.75, 'y': 0.1, 'traceorder':'normal'}

    )

    return sca
