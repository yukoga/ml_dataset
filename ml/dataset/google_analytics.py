# -*- coding: utf-8 -*-
'''
Created on Jul 26, 2016

@author: yukoga
'''

import gav4
import pandas as pd
import re

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from .abstract_dataset import AbstractDataset
import httplib2
from apiclient.errors import HttpError
# from oauth2client import client
# from oauth2client import file
# from oauth2client import tools
# from setuptools.package_index import Credential


class GoogleAnalytics(AbstractDataset):
    '''
    Retrieve data from Google Analytics Core Reporting API.
    Then build and return its pandas.DataFrame.
    '''

    def __init__(self, params=None):
        '''
        Constructor
        '''
        # TODO: exception handling for required parameters.
        self.api_name = params['api_name']
        self.api_version = params['api_version']
        self.scope = params['scope']
        self.key_file = params['key_file_location']
        self.service_account_email = params['service_account_email']

        credentials = ServiceAccountCredentials.from_p12_keyfile(
            self.service_account_email, self.key_file, scopes=self.scope)
        http = credentials.authorize(httplib2.Http())
        self.service = build(self.api_name, self.api_version, http=http)
        self.total = None
        self.features = None
        self.target = None

    def fetch_data(self, query=None):
        if self.api_version is 'v4':
            query = self._build_v4_query(query)
        elif self.api_version is 'v3':
            query = self._build_v3_query(query)
        else:
            raise TypeError('api version must be v3 or v4.')
        self.total = self.fetch_table_data(query, self.service)

    def fetch_table_data(self, query=None, service=None):
        try:
            v4_response = service.reports().batchGet(body=query).execute()
        except HttpError as error:
            print('API error. There was an API error : %s : %s' %
                  (error.resp.status, error._get_reason()))
        rows = v4_response['reports'][0]['data']['rows']
        headers = v4_response['reports'][0]['columnHeader']
        index_col = self.__build_headers_for_dataframe(headers)
        data = self.__transform_rows_for_dataframe(rows)
        return pd.DataFrame(data, columns=index_col)

    def _build_v3_query(self, params):
        if not isinstance(params, dict):
            raise TypeError('query parameters must be dictionary.')
        required_parameters = ['metrics', 'ids', 'start_date', 'end_date']
        if not all([v in params for v in required_parameters]):
            raise TypeError(
                'Query condition should have all '
                'required parameters ids, start_date, end_date, metrics.')
        return params

    def _build_v4_query(self, params):
        if not isinstance(params, dict):
            raise TypeError('query parameters must be dictionary.')
        v3_request = self._build_v3_query(params)
        return gav4.convert_request(**v3_request)

    def __build_headers_for_dataframe(self, headers):
        index_col = []
        if 'dimensions' in headers:
            index_col = headers['dimensions']
        index_col.extend([v.get('name') for v in headers[
            'metricHeader']['metricHeaderEntries']])
        index_col = [re.sub(r'ga:(.*)', r'\1', v) for v in index_col]
        return index_col

    def __transform_rows_for_dataframe(self, rows):
        _table_data = []
        _metrics = [v.get('metrics')[0].get('values') for v in rows]
        _metrics = [map(lambda s: float(s) if re.match(
            r'[0-9]+\.[0-9]+', s) is not None else int(s), l)
                    for l in _metrics]
        if 'dimensions' in rows[0]:
            _table_data = [v.get('dimensions') for v in rows]
            _ = [u.extend(v) for u, v in zip(_table_data, _metrics)]
        else:
            _table_data = _metrics
        return _table_data
