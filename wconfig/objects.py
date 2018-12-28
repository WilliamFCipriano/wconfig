import logging

logger = logging.getLogger('wconfig.objects')


class UninitializedFileError(Exception):

    def __init__(self):
        logger.critical('IOFile init check failed.')


class DevectorizationError(Exception):

    def __init__(self):
        logger.critical('IOFile vectorization failed.')


class KeyNotFoundError(Exception):

    def __init__(self):
        logger.critical('Configuration lookup by key failed. Key not found.')


class Configuration:


    def lookup_by_key(self, search):
        query = search.lower()
        query = query.replace(' ', '_')

        for group in self._vectors:
            for key in self._vectors[group]:
                compare_key = key[0].lower()
                compare_key = compare_key.replace(' ', '_')
                if compare_key == query:
                    return key[1]

        raise KeyNotFoundError

    def __init__(self,IOFile):
        if not IOFile.init_status:
            raise UninitializedFileError

        self._IOFile = IOFile
        self._vectors = IOFile.vectors
        self._group = dict()
        self._statistics = IOFile.statistics

        try:
            for key in IOFile.vectors:

                self._group[key] = IOFile.vectors[key]

                for property in IOFile.vectors[key]:
                    setattr(self, property[0], property[1])

        except (KeyError, TypeError):
            raise DevectorizationError

