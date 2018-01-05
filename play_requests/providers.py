import json
import logging
import re
import requests
from RestrictedPython import RestrictionCapableEval


class RequestsProvider(object):
    """ Requests command provider """

    def __init__(self, engine):
        self.engine = engine
        self.logger = logging.getLogger()

    def _make_auth(self, command):
        """ Update auth on the command """
        self.logger.warning('Not yet implemented')

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
        self.logger.warning('Not yet implemented')

    def _merge_payload(self, command):
        """ Merge command with the default command available in
            self.engine.variables['requests']['default_payload']
        """
        play_requests = self.engine.variables.get('play_requests', {})
        if play_requests:
            default = json.loads(
                self.engine.parametrizer.parametrize(
                    json.dumps(play_requests)))
            if play_requests:
                self._merge(command, default)

    def _merge(self, a, b, path=None):
        """ merges b and a configurations.
            Based on http://bit.ly/2uFUHgb
         """
        if path is None:
            path = []

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self._merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                else:
                    # b wins
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def _make_assertion(self, response, command):
        """ Make an assertion based on python
            expression against the response
        """
        assertion = command.get('assertion', None)
        if assertion:
            self._exec(
                assertion,
                {'response': response,
                 'variables': self.engine.variables,
                 'len': len,
                 'list': list,
                 'match': re.match,
                 }
            )

    def _exec(self, assertion, context):
        """ Make an assertion against a given context
        """

        context = context.copy()
        assert RestrictionCapableEval(assertion).eval(context)

    def _make_request(self, method, command):
        """ Make a request plus assertions """
        cmd = command.copy()
        url = cmd['url']

        self._merge_payload(cmd)
        self._make_auth(cmd)
        self._make_files(cmd)
        self.logger.debug('Requests call %r', cmd)
        if 'parameters' not in cmd:
            cmd['parameters'] = {}

        response = requests.request(
            method,
            url,
            **cmd['parameters'])
        try:
            self._make_assertion(response, cmd)
        except Exception as e:
            self.logger.exception(
                'Exception for command %r',
                cmd,
                e)
            raise e

    def command_OPTIONS(self, command):
        """ OPTIONS command """
        self._make_request('OPTIONS', command)

    def command_HEAD(self, command):
        """ HEAD command """
        self._make_request('HEAD', command)

    def command_GET(self, command):
        """ GET command """
        self._make_request('GET', command)

    def command_POST(self, command):
        """ POST command """
        self._make_request('POST', command)

    def command_PUT(self, command):
        """ PUT command """
        self._make_request('PUT', command)

    def command_PATCH(self, command):
        """ PATCH command """
        self._make_request('PATCH', command)

    def command_DELETE(self, command):
        """ DELETE command """
        self._make_request('DELETE', command)
