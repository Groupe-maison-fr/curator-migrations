from unittest.mock import Mock, ANY

import unittest
from curator_migrations.action_history import define_schema

class TestDefineSchema(unittest.TestCase):

    def test_define_schema_and_delete_index_is_called_if_define_schema_forced(self):
        elasticsearch_client = Mock()
        elasticsearch_client.indices = Mock()
        define_schema(elasticsearch_client, 'aa', True)
        elasticsearch_client.indices.delete.assert_called_once_with(index='aa', ignore=404)
        elasticsearch_client.indices.create.assert_called_once_with(index='aa', ignore=400, settings=ANY, mappings=ANY)
        elasticsearch_client.indices.refresh.assert_called_once_with(index='aa')

    def test_define_schema_and_delete_index_is_not_called_if_define_schema_is_not_forced(self):
        elasticsearch_client = Mock()
        elasticsearch_client.indices = Mock()
        define_schema(elasticsearch_client, 'aa', False)
        elasticsearch_client.indices.delete.assert_not_called()
        elasticsearch_client.indices.create.assert_called_once_with(index='aa', ignore=400, settings=ANY, mappings=ANY)
        elasticsearch_client.indices.refresh.assert_called_once_with(index='aa')


if __name__ == '__main__':
    unittest.main()
