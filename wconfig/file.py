import logging
from string import punctuation
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


class EmptyFileError(Exception):

    def __init__(self, message='INI file contains no data'):
        self.message = message
        logger.critical(message)


class IOFile:
    # This should always be inherited and not called directly

    # setup method, prepare anything you'd do in
    # __init__ here
    def deploy(self):
        pass

    # generate group > key > pair results
    # as a dictionary that points to lists of tuples
    # store this in self.vectorized and return True
    def vectorize(self):
        pass

    def property_validator(self, property):

        if property[0] == '_':
            raise UnrecoverableParserError("Properties can not begin with _.")

        for char in property:
            if char == '_':
                continue

            if char in punctuation:
                raise UnrecoverableParserError("Invalid character '%s' detected in property." % char)

        return property

    def value_validator(self, value):

        if value.upper() is 'TRUE':
            return True

        if value.upper() is 'FALSE':
            return False

        return value



    def __init__(self, location):

        # Interface
        self.vectorized = list()
        self.init_status = False
        self.statistics = dict()
        self.statistics['path'] = location

        # Internal
        self._cur_group = 'root'

        # Verify that the file exists
        if not os.path.isfile(location):
            raise UnrecoverableIOError('File %s does not exist' % location)

        # Gather file statistics
        self.statistics['path'] = location
        self.statistics['abspath'] = os.path.abspath(location)
        self.statistics['size'] = os.path.getsize(location)

        if self.statistics['size'] == 0:
            raise EmptyFileError()

        try:
            self.statistics['file_last_modified'] = os.path.getmtime(location)
        except Exception as ex:
            logger.warning('Get modified time failed with: %s', ex)
            self.last_modified = False

        # Load configuration file
        try:
            logging.debug('Reading configuration file from: %s', location)
            f = open(location)
            self.content = f.read()
            self.statistics['total_lines'] = self.content.count('\n') + 1
            f.close()
        except Exception as ex:
            logger.warning('INI file loading failed with: %s', ex)
            raise UnrecoverableIOError

        # Run deploy method, and then vectorize method
        try:
            if self.deploy():
                if self.vectorize():
                    self.init_status = True
        except Exception as ex:
            raise UnrecoverableParserError('Parser error: %s' % str(ex))


class INI(IOFile):

    # Called at object initialization
    def deploy(self):
        self.statistics['relevant_lines'] = 0
        self.statistics['has_groups'] = False
        self.statistics['total_entries'] = 0
        self.statistics['skipped_lines'] = 0
        return True

    # Called directly after deploy()
    def vectorize(self):
        cache = self.content.split('\n')
        rendered = dict()
        rendered[self._cur_group] = list()

        for item in cache:
            if len(item) == 0:
                continue

            if item[0] not in ('#', ';'):
                if item[0] == '[':
                    if item[len(item) - 1] == ']':
                        self.statistics['has_groups'] = True
                        self._cur_group = item[1:-1]
                        rendered[self._cur_group] = list()

                elif '=' in item:
                    rendered[self._cur_group].append(self.render_line(item, '='))
                    self.statistics['total_entries'] += 1

                elif ':' in item:
                    rendered[self._cur_group].append(self.render_line(item, ':'))
                    self.statistics['total_entries'] += 1
                else:
                    self.statistics['skiped_lines'] += 1

        if rendered == {'root': []}:
            raise UnrecoverableParserError('Invalid file.')

        self.vectors = rendered

        # basic sanity check
        if self.statistics['total_entries'] >= 1:
            return True
        else:
            return False

    # Specific to this implementation
    # not generally required
    def render_line(self, line, specialchar):
        self.statistics['relevant_lines'] += 1

        specialchar_with_space = ' %s ' % specialchar
        if specialchar_with_space in line:
            line = line.split(specialchar_with_space)
            self.statistics['whitespace_around_equals'] = True
        else:
            line = line.split(specialchar)
            self.statistics['whitespace_around_equals'] = False

        return self.property_validator(line[0]), self.value_validator(line[1])