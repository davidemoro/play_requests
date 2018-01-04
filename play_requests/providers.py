class RequestsProvider(object):
    """ Print provider """

    def __init__(self, engine):
        self.engine = engine

    def _make_auth(self, command):
        """ Returns the auth object """
        raise NotImplementedError

    def _make_file(self, command):
        """ Returns the file object for a given path """
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
