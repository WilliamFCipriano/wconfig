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

    def __init__(self, vectorized=basic_statistics_mock_data, location='test-files/basic.ini', statistics=basic_statistics_mock_data, init_status = True):
        self.vectorized = vectorized
        self.init_status = init_status
        self.statistics = statistics
        self.statistics['path'] = location


def test_fail_safe_handling():

    mock = file_mock(init_status=False)

    with pytest.raises(objects.UninitializedFileError):
        objects.Configuration(mock)


def test_statistics():

    mock = file_mock()
