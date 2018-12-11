import logging
import os

logger = logging.getLogger('wconfig.file')


class UnrecoverableIOError(Exception):

    def __init__(self, message):
        self.message = message
        logger.critical(message)


class UnrecoverableParserError(Exception):

    def __init__(self, message):
        self.message = message
        logger.critical(message)


class INI:

    def vectorize(self):
        cache = self.content.split('\n')
        rendered = list()

        for item in cache:
            if item[0] != '#':
                if '=' in item:
                    rendered.append(item)

        self.vectors = rendered

        return True


    def __init__(self, location):

        self.cursor = 0
        self.vectorized = list()

        if not os.path.isfile(location):
            logger.warning('INI file at %s does not exist!', location)
            raise UnrecoverableIOError('File %s does not exist' % location)

        try:
            self.last_modified = os.path.getmtime(location)
        except Exception as ex:
            logger.warning('Get modified time failed with: %s', ex)
            self.last_modified = False

        try:
            logging.debug('Reading configuration file from: %s', location)
            f = open(location)
            self.content = f.read()
            f.close()
        except Exception as ex:
            logger.warning('INI file loading failed with: %s', ex)
            raise UnrecoverableIOError

        try:
            self.vectorize()
        except Exception as ex:
            logger.warning('INI file parsing failed with: %s', ex)
            raise UnrecoverableParserError

