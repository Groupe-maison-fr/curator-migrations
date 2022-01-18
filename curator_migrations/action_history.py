from datetime import datetime
from elasticsearch import exceptions


def define_schema(elasticsearch_client, index_name, force_index_creation):
    if force_index_creation:
        elasticsearch_client.indices.delete(
            index=index_name,
            ignore=404
        )
    elasticsearch_client.indices.create(
        index=index_name,
        ignore=400,
        settings={
            'index': {
                'number_of_shards': 2,
                'number_of_replicas': 1
            }
        },
        mappings={
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'text'
                },
                'status': {
                    'type': 'keyword'
                },
                'started_at': {
                    'type': 'date'
                },
                'ended_at': {
                    'type': 'date'
                },
                'log': {
                    'type': 'text'
                }
            }
        }
    )

    elasticsearch_client.indices.refresh(
        index=index_name
    )


def is_action_done(elasticsearch_client, index_name, migration_script_id, override_running_state):
    try:
        action_history = elasticsearch_client.get(
            index=index_name,
            id=migration_script_id
        )
        if action_history['_source']['status'] == 'success':
            return True

        if action_history['_source']['status'] == 'running' and override_running_state:
            return False

        raise Exception('action "%s" in "%s" is already in state: "%s"' % (
            migration_script_id,
            index_name, action_history['_source']['status']
        ))

    except exceptions.NotFoundError:
        return False


def action_start(elasticsearch_client, index_name, migration_script_id):
    try:
        elasticsearch_client.create(
            index=index_name,
            id=migration_script_id,
            document={
                'status': 'running',
                'started_at': datetime.now()
            }
        )
        return True
    except exceptions.ConflictError:
        elasticsearch_client.update(
            index=index_name,
            id=migration_script_id,
            doc={
                'status': 'running',
                'started_at': datetime.now()
            }
        )
        return True
    except exceptions.NotFoundError:
        return False


def action_end(elasticsearch_client, index_name, migration_script_id, log):
    try:
        elasticsearch_client.update(
            index=index_name,
            id=migration_script_id,
            doc={
                'status': 'success',
                'ended_at': datetime.now(),
                'log': log,
            }
        )
        return True
    except exceptions.NotFoundError:
        return False
