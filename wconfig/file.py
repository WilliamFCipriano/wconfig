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


class IllegalParserError(Exception):

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
        logger.critical('deploy method has not been configured')
        pass

    # generate group > key > pair results
    # as a dictionary that points to lists of tuples
    # store this in self.vectorized and return True
    def vectorize(self):
        logger.critical('vectorize method has not been configured')
        pass

    def property_validator(self, property):

        if len(property) == 0:
            raise IllegalParserError("Property length can't be zero.")

        if property[0] == '_':
            raise IllegalParserError("Properties can not begin with _.")

        for char in property:
            if char == '_':
                continue

            if char in punctuation:
                logger.critical('property: "%s" contains invalid character' % property)
                raise IllegalParserError("Invalid character '%s' detected in property." % char)

        return property



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


        self.statistics['file_last_modified'] = os.path.getmtime(location)


        # Load configuration file
        logging.debug('Reading configuration file from: %s', location)
        f = open(location)
        self.content = f.read()
        self.statistics['total_lines'] = self.content.count('\n') + 1
        f.close()


        # Run deploy method, and then vectorize method
        if self.deploy():
            if self.vectorize():
                self.init_status = True


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
                        continue

                # As = or : can be used as an operator
                # we have to do some magic to figure out what one
                # the file is trying to do.
                if item.find('=') != -1:
                    if item.find(':') == -1:
                        rendered[self._cur_group].append(self.render_line(item, '='))
                        self.statistics['total_entries'] += 1
                        continue
                    else:
                        if item.find('=') < item.find(':'):
                            rendered[self._cur_group].append(self.render_line(item, '='))
                            self.statistics['total_entries'] += 1
                            continue


                if item.find(':') != -1:
                    if item.find('=') == -1:
                        rendered[self._cur_group].append(self.render_line(item, ':'))
                        self.statistics['total_entries'] += 1
                        continue
                    else:
                        if item.find(':') < item.find('='):
                            rendered[self._cur_group].append(self.render_line(item, ':'))
                            self.statistics['total_entries'] += 1
                            continue

                self.statistics['skipped_lines'] += 1

        if rendered == {'root': []}:
            raise UnrecoverableParserError("File '%s' is invalid. (%s)" % (self.statistics['path'], self.statistics['abspath']))

        self.vectors = rendered

        # basic sanity check
        if self.statistics['total_entries'] >= 1:
            return True

    # Specific to this implementation
    # not generally required
    def render_line(self, line, specialchar):
        self.statistics['relevant_lines'] += 1

        specialchar_with_space = ' %s ' % specialchar

        space_loc = line.find(specialchar_with_space)
        no_space_loc = line.find(specialchar)



        if space_loc != -1:
            if space_loc < no_space_loc:
                data = line.split(specialchar_with_space, 1)
                self.statistics['whitespace_around_equals'] = True
        else:
            data = line.split(specialchar, 1)
            self.statistics['whitespace_around_equals'] = False

        return self.property_validator(data[0]), data[1]


