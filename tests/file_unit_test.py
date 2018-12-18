import pytest
import os
import random
import string
from wconfig import file

# basic.ini
example_ini_file = file.INI('test-files/basic.ini')

seed = random.randint(1, 99999)
random.seed(seed)


# INI fuzzer test prep
def generate_random_key_pair():
    key_length = random.randint(1, 100)
    value_length = random.randint(1, 255)
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_length))
    value = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(value_length))
    return key, value


def generate_random_comment():
    comment_length = random.randint(1, 100)
    comment = ''.join(random.choice(string.ascii_letters + string.punctuation + string.digits) for _ in range(comment_length))
    if random.randint(1, 2) == 1:
        return '#' + comment
    else:
        return ';' + comment


class RandomINI():

    def __init__(self, length=10, valid=True):

        self.output = ''
        self.length = length
        self.valid = valid

        self.keypairs = dict()

        length = random.randint(100, 5000)

        x = 0
        while x < length:
            rand = random.randint(1, 3)

            if rand == 1:
                key_pair = generate_random_key_pair()
                self.keypairs[key_pair[0]] = key_pair[1]
                if random.randint(1, 10) >= 5:
                    self.output += ('%s=%s\n' % (key_pair[0], key_pair[1]))
                else:
                    if random.randint(1, 10) >= 5:
                        self.output += ('%s = %s\n' % (key_pair[0], key_pair[1]))
                    else:
                        self.output += ('%s:%s\n' % (key_pair[0], key_pair[1]))

            if rand == 2:
                self.output += '%s\n' % generate_random_comment()

            if rand == 3:
                if not valid:
                    invalid_length = random.randint(1, 1000)
                    invalid_entry = ''.join(random.choice(string.printable) for _ in range(invalid_length))
                    self.output += ('%s\n' % invalid_entry)
            x += 1

    def create_file(self, location):
        self.location = location
        f = open(location, 'w')
        f.write(self.output)

    def clean_up(self):
        os.remove(self.location)


# Start tests
def test_fileio_read():
    assert example_ini_file.content == open('test-files/basic.ini').read(), \
        'Failure to accurately read from disk with basic.ini'


def test_basic_ini_content():

    # content check
    assert example_ini_file.vectors['root'][0] == ('this_is_a_test', 'of the parser'), \
        'Failure to parse line 1 of basic.ini'
    assert example_ini_file.vectors['root'][1] == ('see', 'here'), \
        'Failure to parse line 2 of basic.ini'
    assert example_ini_file.vectors['group name'][0] == ('more', 'stuff'), \
        'Failure to parse line 4 of basic.ini'
    assert example_ini_file.vectors['group name'][1] == ('right', 'here'), \
        'Failure to parse line 5 of basic.ini'
    assert example_ini_file.vectors['another group'][0] == ('more', 'stuff'), \
        'Failure to parse line 8 of basic.ini'
    assert example_ini_file.vectors['another group'][1] == ('it_can_overlap', 'yes sirrr'), \
        'Failure to parse line 9 of basic.ini'
    assert example_ini_file.vectors['another group'][2] == ('this_here','is something'), \
        'Failure to parse line 12 of basic.ini'
    assert example_ini_file.vectors['this group is something'][0] == ('but_this', 'is too!'), \
        'Failure to parse line 14 of basic.ini'


def test_basic_ini_statistics():

    # statistics check
    assert example_ini_file.statistics['path'] == 'test-files/basic.ini', \
        'Failure to collect correct path statistic while parsing basic.ini'
    assert example_ini_file.statistics['total_lines'] is 15, \
        'Failure to collect correct total_lines statistic while parsing basic.ini'
    assert example_ini_file.statistics['relevant_lines'] is 8, \
        'Failure to collect correct relevant_lines statistic while parsing basic.ini'
    assert example_ini_file.statistics['has_groups'] is True, \
        'Failure to collect correct has_groups statistic while parsing basic.ini'
    assert example_ini_file.statistics['total_entries'] is 8, \
        'Failure to collect correct total_entries statistic while parsing basic.ini'
    assert example_ini_file.statistics['skipped_lines'] is 0, \
        'Failure to collect correct skipped_lines statistic while parsing basic.ini'
    assert example_ini_file.statistics['whitespace_around_equals'] is False, \
        'Failure to collect correct whites_around_equals statistic while parsing basic.ini'


# Negative testing
def test_basic_ini_unrecoverableioerror():
    # error handling: ini file does not exist
    with pytest.raises(file.UnrecoverableIOError):
        file.INI('test-files/BADPATH.ini')


def test_basic_ini_emptyfileerror():
    # error handling: ini file contains no data
    with pytest.raises(file.EmptyFileError):
        file.INI('test-files/blankfile.ini')


def test_basic_ini_unrecoverableparsererror():
    # error handling: ini file has mass but no data
    with pytest.raises(file.UnrecoverableParserError):
        file.INI('test-files/broken.ini')


def test_basic_ini_illegalparsererror():
    # error handling: ini file has a bad property
    with pytest.raises(file.IllegalParserError):
        file.INI('test-files/badproperty.ini')


def test_io_file_property_validator():
    # error handling: property name begins with underscore
    with pytest.raises(file.IllegalParserError):
        example_ini_file.property_validator('_test')

    # error handling: property contains invalid characters
    with pytest.raises(file.IllegalParserError):
        example_ini_file.property_validator('propertname!!!')


def test_ini():
    # General test cases
    example_ini_file = file.INI('test-files/test.ini')

    # root test
    assert 'root' in example_ini_file.vectors

    # colon testing
    assert 'colon_test' in example_ini_file.vectors, \
        'Failure to parse colon group in test.ini'

    test_data = example_ini_file.vectors['colon_test']

    assert test_data[0] == ('colon_no_space','value'), \
        'Failure to parse colon_no_space value in colon_test'
    assert test_data[1] == ('colon_with_space', 'value'), \
        'Failure to parse colon_with_space value in colon_test'
    assert test_data[2] == ('equals_after_colon_with_no_space', 'value'), \
        'Failure to parse equals_after_colon_with_no_space value in colon_test'
    assert test_data[3] == ('equals_after_the_equals_after_the_colon_with_no_space', 'value'), \
        'Failure to parse equals_after_the_equals_after_the_colon_with_no_space value in colon_test'
    assert test_data[4] == ('guess_whos_back', 'backstreet'), \
        'Failure to parse guess_whos_back value in colon_test'

def test_object_conformance():
    test_object = file.IOFile('test-files/basic.ini')

    test_object.deploy()
    test_object.vectorize()

    with pytest.raises(file.IllegalParserError):
        test_object.property_validator('')


def test_fuzz_ini():
    # Fuzz testing
    fuzzy_ini = RandomINI()
    fuzzy_ini.create_file('fuzz.ini')

    try:
        parsed_ini = file.INI('fuzz.ini')
    except file.IllegalParserError:
        pytest.fail('Parser failure with seed: "%s"' % seed)

    for key, value in parsed_ini.vectorized:
        assert fuzzy_ini.keypairs[key] == value, \
            'Fuzzed ini parser failure with seed: "%s"'

    bad_ini = RandomINI(valid=False)
    bad_ini.create_file('bad.ini')

    with pytest.raises(file.IllegalParserError):
        file.INI('bad.ini')

    fuzzy_ini.clean_up()
    bad_ini.clean_up()








