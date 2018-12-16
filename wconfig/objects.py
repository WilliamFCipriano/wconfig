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

        self._statistics = IOFile.statistics

        for vector in IOFile.vectorized:
            setattr(self, vector[0], vector[1])



