class RequestsProvider(object):
    """ Requests command provider """

    def __init__(self, engine):
        self.engine = engine

    def _make_auth(self, command):
        """ Returns the auth object """
        raise NotImplementedError

    def _make_files(self, command):
        """ Returns the file object for a given path """
        raise NotImplementedError

    def _merge_payload(self, parameters):
        """ Return merged command parameters
            with the default payload available in
            self.engine.variables['requests']['default_payload']
        """
        raise NotImplementedError

    def _make_assertion(self, response, assertion):
        """ Make an assertion based on python
            expression against the response
        """
        raise NotImplementedError

    def command_head(self, command):
        raise NotImplementedError

    def command_get(self, command):
        raise NotImplementedError

    def command_post(self, command):
        # raise NotImplementedError
        pass

    def command_put(self, command):
        raise NotImplementedError

    def command_patch(self, command):
        raise NotImplementedError

    def command_delete(self, command):
        raise NotImplementedError
