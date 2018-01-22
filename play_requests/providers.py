import json
import logging
import re
import requests
from pytest_play.providers import BaseProvider


class RequestsProvider(BaseProvider):
    """ Requests command provider """

    def __init__(self, engine):
        super(RequestsProvider, self).__init__(engine)
        self.logger = logging.getLogger()

    def _make_auth(self, command):
        """ Update auth on the command """
        self.logger.warning('auth not yet implemented')

    def _make_files(self, command):
        """ Update files on the command

            requests accept parameters like that::

                files = {
                    'file': (
                        'report.xls',
                        open('report.xls', 'rb'),
                        'application/vnd.ms-excel',
                        {'Expires': '0'}
                    )
                }

            or::

                files = {
                    'file': (
                        'report.csv',
                        'some,data\nanother,row\n')}
        """
        parameters = command.get('parameters', {})
        files = parameters.get('files', {})
        if files:
            results = {}
            for key, value in files.items():
                filename = value[0]
                file_data = value[1]
                additional_args = value[2:]
                match = re.search(r'path:([^$]+)', file_data)
                if match:
                    file_path = match.group(1)
                    file_data = open(file_path, 'rb')
                if additional_args:
                    results[key] = (filename, file_data, value[2:])
                else:
                    results[key] = (filename, file_data)
            command['parameters']['files'] = results

    def _make_cookies(self, command):
        """ Update cookies on the command """
        self.logger.warning('cookies not yet implemented')

    def _make_assertion(self, command, **kwargs):
        """ Make an assertion based on python
            expression against kwargs
        """
        assertion = command.get('assertion', None)
        if assertion:
            self.engine.execute_command(
                {'provider': 'python',
                 'type': 'assert',
                 'expression': assertion
                 },
                **kwargs,
            )

    def _make_variable(self, command, **kwargs):
        """ Make a variable based on python
            expression against kwargs
        """
        expression = command.get('variable_expression', None)
        if expression:
            self.engine.execute_command(
                {'provider': 'python',
                 'type': 'store_variable',
                 'name': command['variable'],
                 'expression': expression
                 },
                **kwargs,
            )

    def _make_request(self, method, command):
        """ Make a request plus assertions """
        cmd = command.copy()
        url = cmd['url']

        self._make_auth(cmd)
        self._make_files(cmd)
        self.logger.debug('Requests call %r', cmd)
        if 'parameters' not in cmd:
            cmd['parameters'] = {}

        self.logger.debug('Effective HTTP call %r', cmd)
        response = requests.request(
            method,
            url,
            **cmd['parameters'])
        try:
            self._make_variable(cmd, response=response)
            self._make_assertion(cmd, response=response)
        except Exception as e:
            self.logger.exception(
                'Exception for command %r',
                cmd,
                e)
            raise e

    def command_OPTIONS(self, command, **kwargs):
        """ OPTIONS command """
        self._make_request('OPTIONS', command)

    def command_HEAD(self, command, **kwargs):
        """ HEAD command """
        self._make_request('HEAD', command)

    def command_GET(self, command, **kwargs):
        """ GET command """
        self._make_request('GET', command)

    def command_POST(self, command, **kwargs):
        """ POST command """
        self._make_request('POST', command)

    def command_PUT(self, command, **kwargs):
        """ PUT command """
        self._make_request('PUT', command)

    def command_PATCH(self, command, **kwargs):
        """ PATCH command """
        self._make_request('PATCH', command)

    def command_DELETE(self, command, **kwargs):
        """ DELETE command """
        self._make_request('DELETE', command)
