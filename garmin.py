# extract garmin data
from garminconnect import Garmin
import pandas as pd
from datetime import date as dt

def get_garmin_data(username,password):

    try:

        # input: username and passwrod
        # output: normalised pandas df containing garmain connect data of username

        # connect garmin client
        client = Garmin(username, password)
        client.login()
        activities = client.get_activities(0, 1000)

        # store as dataframe
        df = pd.DataFrame(activities)
        # make data useable
        wanted = ['activityId','activityName','startTimeLocal','distance',
                'duration','elevationGain','elevationLoss',
                'averageSpeed','maxSpeed','calories',
                'averageHR','maxHR','averageRunningCadenceInStepsPerMinute',
                'averageBikingCadenceInRevPerMinute','averageSwimCadenceInStrokesPerMinute',
                'aerobicTrainingEffect','anaerobicTrainingEffect']

        df = df[df.columns.intersection(wanted)]
        df['duration'] = df['duration'].div(60).round(2)
        df['activityType'] = df['activityName'].str.split(' ').str[-1]
        df['startTimeLocal'] = pd.to_datetime(df['startTimeLocal'], errors='coerce')
        df['startTimeLocal'] = df['startTimeLocal'].dt.date
    
        return ["Success", df]

    except:
        return ["Garmin Login Error"]
