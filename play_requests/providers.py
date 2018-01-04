import logging
import requests


class RequestsProvider(object):
    """ Requests command provider """

    def __init__(self, engine):
        self.engine = engine
        self.logger = logging.getLogger()

    def _make_auth(self, command):
        """ Returns the auth object """
        pass

    def _make_files(self, command):
        """ Returns the file object for a given path """
        pass

    def _merge_payload(self, command):
        """ Merge command with the default command available in
            self.engine.variables['requests']['default_payload']
        """
        pass

    def _make_assertion(self, response, assertion):
        """ Make an assertion based on python
            expression against the response
        """
        pass

    def _make_request(self, method, command):
        """ Make a request plus assertions """
        cmd = command.copy()
        url = cmd['url']
        method = cmd['type']
        assertion = cmd.get('assertion', {})

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
        if assertion:
            try:
                self._make_assertion(response, assertion)
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
        self._make_request('POST', command)

    def command_GET(self, command):
        """ GET command """
        self._make_request('POST', command)

    def command_POST(self, command):
        """ POST command """
        self._make_request('POST', command)

    def command_PUT(self, command):
        """ PUT command """
        self._make_request('POST', command)

    def command_PATCH(self, command):
        """ PATCH command """
        self._make_request('POST', command)

    def command_DELETE(self, command):
        """ DELETE command """
        self._make_request('POST', command)
