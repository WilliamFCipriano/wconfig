import pytest
from wconfig import file


def test_basic_ini():

    # basic.ini
    example_ini_file = file.INI('test-files/basic.ini')
    assert example_ini_file.statistics['total_lines'] == 13
    assert example_ini_file.vectors['root'][0] == ('this_is_a_test', 'of the parser')
    assert example_ini_file.statistics['has_groups'] == True
    assert example_ini_file.statistics['relevant_lines'] == 8
    assert example_ini_file.vectors['group name'][0] == ('more', 'stuff')

    # ini file does not exist
    with pytest.raises(file.UnrecoverableIOError):
        file.INI('test-files/BADPATH.ini')

    # ini file contains no data
    with pytest.raises(file.EmptyFileError):
        file.INI('test-files/blankfile.ini')

    # ini file is malformed
    with pytest.raises(file.UnrecoverableParserError):
        print(file.INI('test-files/broken.ini'))


def test_advanced_ini():

    example_ini_file = file.INI('test-files/advanced.ini')