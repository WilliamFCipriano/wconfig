import pytest
from wconfig import objects

basic_statistics_mock_data = {'path': 'basic.ini', 'abspath': 'C:\\code\\wconfig\\tests\\basic.ini', 'size': 240,
                              'file_last_modified': 1544501341.19, 'total_lines': 13, 'relevant_lines': 8,
                              'has_groups': True, 'whitespace_around_equals': False}


basic_vectors_mock_data = {'root': [('this_is_a_test', 'of the parser'), ('see', 'here')],
                           'group name': [('more', 'stuff'), ('right', 'here')],
                           'another group': [('more', 'stuff'), ('it_can_overlap', 'yes sirrr'),
                           ('this_here', 'is something')], 'this group is something': [('but_this', 'is too!')]}

class file_mock:

    def __init__(self, vectorized=basic_vectors_mock_data, location='test-files/basic.ini',
                 statistics=basic_statistics_mock_data, init_status = True):
        self.vectorized = vectorized
        self.init_status = init_status
        self.statistics = statistics
        self.statistics['path'] = location

def test_fail_safe_handling():

    mock = file_mock(init_status=False)

    with pytest.raises(objects.UninitializedFileError):
        objects.Configuration(mock)


def test_basic_ini_statistics():

    mock = file_mock()
    test_configuration = objects.Configuration(mock)

    assert test_configuration._statistics['path'] == 'test-files/basic.ini', \
        'Configuraton object path statistic parse failure'
    assert test_configuration._statistics['abspath'] == 'C:\\code\\wconfig\\tests\\basic.ini', \
        'Configuration object abspath statistic parse failure'
    assert test_configuration._statistics['size'] == 240, \
        'Configuration object size statistic parse failure'
    assert test_configuration._statistics['file_last_modified'] == 1544501341.19, \
        'Configuration object file_last_modified statistic parse failure'
    assert test_configuration._statistics['total_lines'] == 13, \
        'Configuration object total_lines statistic parse failure'
    assert test_configuration._statistics['relevant_lines'] == 8, \
        'Configuration object relevant_lines statistic parse failure'


def test_basic_ini_vectors():

    mock = file_mock()
    test_configuration = objects.Configuration(mock)

    for key in basic_vectors_mock_data:

        assert test_configuration._group[key] == basic_vectors_mock_data[key]

        for property in basic_vectors_mock_data[key]:
            assert hasattr(test_configuration, property[0]), \
                'configuration object parser failure property "%s"' % property[0]
            assert test_configuration.__dict__[property[0]] == property[1], \
                'configuration object parser failure property "%s"' \
                'does not have key "%s".' % (property[0], property[1])


