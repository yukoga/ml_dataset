# -*- coding: utf-8 -*-
'''
Created on Jul 26, 2016

@author: yukoga
'''
from ml.dataset.google_analytics import GoogleAnalytics
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#%%


class Visualizer(object):

    def __init__(self):
        sns.set_style("darkgrid")

    def plot_histgram(self, x=None, y=None, data=None):
        pass

    def plot_scatter(self, x=None, y=None, data=None):
        pass

    def plot_timeseries(self, x=None, y=None, unit=None, data=None):
        #        _timeseries = data[x]
        #        _value = data[y]
        sns.tsplot(data, time=x, unit=unit, value=y)
#        sns.tsplot(data, time=_timeseries, value=_value)

#%%


def get_data_from_api(google_analytics_obj=None, query=None):
    google_analytics_obj.fetch_data(query)
    return google_analytics_obj.total


def visualize_data(data, chart_type=None, x=None, y=None):
    charts = ['histgram', 'scatter', 'timeseries']
    vz = Visualizer()
    if chart_type not in charts:
        raise TypeError(
            'chart_type must be one of histgram, scatterplot, timeseries')

    getattr(vz, 'plot_' + chart_type)(x, y, data)

#%%


def main():
    params = {}
    params['api_name'] = 'analyticsreporting'
    params['api_version'] = 'v4'
    params['scope'] = 'https://www.googleapis.com/auth/analytics.readonly'
    params['service_account_email'] = \
        'yukoga-analytics-api@gcp-jp.iam.gserviceaccount.com'
    params['key_file_location'] = '/Users/yukoga/workspace/python/dummy/gcp-jp.p12'
    ga = GoogleAnalytics(params=params)
    query_params = {
        'ids': 'ga:114540399',  # 92320289 for Google Analytics demo account.
        'start_date': '2016-01-01',
        'end_date': '2016-07-20',
                    'dimensions': 'ga:date,ga:hour',
                    'metrics': 'ga:sessions,ga:pageviews,ga:bounceRate,ga:avgSessionDuration'
    }
    data = get_data_from_api(google_analytics_obj=ga, query=query_params)
    data.column = ['date', 'hour', 'sessions', 'pageviews']
    data['date_hour'] = pd.to_datetime(
        data.date +
        data.hour.apply(
            lambda x: x.ljust(
                4,
                '0')))
    return data
#    visualize_data(data, chart_type='timeseries', x='date_hour', y='sessions')

#%%
if __name__ == '__main__':
    data = main()
    print(data.head())
#    visualize_data(data=data, chart_type='timeseries', x='date_hour', y='sessions', unit='date')
