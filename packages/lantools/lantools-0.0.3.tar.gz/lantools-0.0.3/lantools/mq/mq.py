class Reader:
    def __init__(self, options):
        self.options = options

    def run(self, callback):
        pass

class Writer:
    def write(self, message, *, callback=None):
        pass
