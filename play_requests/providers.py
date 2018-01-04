class NewProvider(object):
    """ Print provider """

    def __init__(self, engine):
        self.engine = engine

    def command_print(self, command):
        print(command['message'])

    def command_yetAnotherCommand(self, command):
        pass
