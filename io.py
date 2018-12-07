import logging


class FileIOError(Exception):
    pass


class ConfigurationFile:

    def __init__(self, location):
        self.location = location
        try:
            f = open(location)
            self.content = f.read()
        except Exception as ex:
            logging.warning('Configuration file loading failed with: %' % str(ex))
            raise FileIOError
