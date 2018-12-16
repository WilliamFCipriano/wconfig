import pytest
from wconfig import file


def test_basic_ini():

    # basic.ini
    example_ini_file = file.INI('test-files/basic.ini')

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

    # statistics check
    assert example_ini_file.statistics['path'] is 'test-files/basic.ini', \
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

    # error handling: ini file does not exist
    with pytest.raises(file.UnrecoverableIOError):
        file.INI('test-files/BADPATH.ini')

    # error handling: ini file contains no data
    with pytest.raises(file.EmptyFileError):
        file.INI('test-files/blankfile.ini')

    # error handling: ini file has mass but no data
    with pytest.raises(file.UnrecoverableParserError):
        file.INI('test-files/broken.ini')

    # error handling: ini file has a bad property
    with pytest.raises(file.IllegalParserError):
        file.INI('test-files/badproperty.ini')


def test_ini():

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





