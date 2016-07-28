# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pytest
from ml.dataset.google_analytics import GoogleAnalytics
from warnings import warn


@pytest.fixture
def data():
    try:
        params = {}
        params['api_name'] = 'analyticsreporting'
        params['api_version'] = 'v4'
        params['scope'] = 'https://www.googleapis.com/auth/analytics.readonly'
        params['service_account_email'] = \
            'yukoga-analytics-api@gcp-jp.iam.gserviceaccount.com'
        params['key_file_location'] = './gcp-jp.p12'
        ga = GoogleAnalytics(params=params)
        query_params = {
            # You need to specify your own Google Analytics View ID.
            'ids': 'ga:114540399',
            'start_date': '2016-01-01',
            'end_date': '2016-07-20',
            'dimensions': 'ga:date,ga:hour',
            'metrics': 'ga:sessions,ga:pageviews'
        }
        ga.fetch_data(query_params)
        return ga
    except TypeError:
        warn('Failed to fetch Google Analytics data. {}'
             .format(TypeError))


def test_googleanalytics_instantiation(data):
    # check if data type is correct.
    assert isinstance(data, GoogleAnalytics)
    assert isinstance(data.total, pd.DataFrame)
#    assert isinstance(data.features, pd.DataFrame)
#    assert isinstance(data.target, pd.Series)


def test_googleanalytics_data_shape(data):
    num_columns = 4  # ['ga:date', 'ga:hour', 'ga:sessions', 'ga:pageviews']
    num_records = 1000  # should have 1000 records for test dataset.
    assert len(data.total) == num_records
    assert len(data.total.T) == num_columns


def test_googleanalytics_data_summary(data):
    # You must set DataFrame data based on your query_params.
    expected_summary_df = pd.DataFrame([
                                        # number of records results from API query.
                                        [1000.000000, 1000.000000],
                                        # mean.
                                        [1.706000, 2.159000],
                                        # std.
                                        [1.144934, 1.747791],
                                        # min.
                                        [0.000000, 1.000000],
                                        # 25%.
                                        [1.000000, 1.000000],
                                        # 50%.
                                        [1.000000, 2.000000],
                                        # 75%.
                                        [2.000000, 3.000000],
                                        # max.
                                        [11.000000, 15.000000]])
    expected_summary_df.index = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    expected_summary_df.columns = ['sessions', 'pageviews']

    assert data.total.describe().equals(expected_summary_df)
