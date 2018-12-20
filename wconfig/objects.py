import logging

logger = logging.getLogger('wconfig.objects')


class UninitializedFileError(Exception):

    def __init__(self):
        logger.critical('IOFile init check failed.')


class DevectorizationError(Exception):

    def __init__(self):
        logger.critical('IOFile vectorization failed.')


class Configuration:

    def __init__(self,IOFile):
        if not IOFile.init_status:
            raise UninitializedFileError

        self._group = dict()
        self._statistics = IOFile.statistics

        try:
            for key in IOFile.vectorized:

                self._group[key] = IOFile.vectorized[key]

                for property in IOFile.vectorized[key]:
                    setattr(self, property[0], property[1])

        except KeyError:
            raise DevectorizationError

