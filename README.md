# Curator migrations

![CI](https://github.com/Groupe-maison-fr/curator-migrations/actions/workflows/ci.yml/badge.svg)

Curator migrations offer additional functionality on top of curator:
 - persists log of executed actions, with start/end dates as an history
 - play only not already played ones by maintaining a dedicated index.
 - environment variables substitution in action files (pay attention to `ES_INDEX_PREFIX` in `actionxxxx.yaml` )

## Installation
```
pip install git+git://github.com/groupe-maison-fr/curator-migrations.git
```

## Command options
```
usage: curatorMigrations [-h] [--elasticsearch-host ELASTICSEARCH_HOST]
                         [--elasticsearch-port ELASTICSEARCH_PORT]
                         [--action-files-path ACTION_FILES_PATH]
                         [--action-history-index-name ACTION_HISTORY_INDEX_NAME]
                         [--force-index-creation FORCE_INDEX_CREATION]
                         [--override-running-state OVERRIDE_RUNNING_STATE]
                         [--config-file CONFIG_FILE] [--dry-run DRY_RUN]

Run curator actions sequentially as in doctrine migrations

optional arguments:
  -h, --help            show this help message and exit
  --elasticsearch-host ELASTICSEARCH_HOST
                        elasticsearch host
  --elasticsearch-port ELASTICSEARCH_PORT
                        elasticsearch port
  --action-files-path ACTION_FILES_PATH
                        path of action files
  --action-history-index-name ACTION_HISTORY_INDEX_NAME
                        index name of actions history
  --force-index-creation FORCE_INDEX_CREATION
                        force creation of index of actions history
  --override-running-state OVERRIDE_RUNNING_STATE
                        force execution even if history action is in running
                        state
  --config-file CONFIG_FILE
                        curator.yml configuration file
  --dry-run DRY_RUN     dry-run
```

## Example of executions:

```
$ ES_INDEX_PREFIX=test_ curatorMigrations \
	--elasticsearch-host=rkt-elasticsearch\
	--action-files-path=./samples/actions/\
	--config-file=samples/curator.yml

2021-12-08 06:51:05,657 INFO      GET http://rkt-elasticsearch:9200/ [status:200 request:0.003s]
2021-12-08 06:51:05,772 INFO      PUT http://rkt-elasticsearch:9200/action_history [status:200 request:0.115s]
2021-12-08 06:51:05,775 INFO      POST http://rkt-elasticsearch:9200/action_history/_refresh [status:200 request:0.002s]
2021-12-08 06:51:05,781 WARNING   GET http://rkt-elasticsearch:9200/action_history/_doc/action20211204120000.yaml [status:404 request:0.003s]
2021-12-08 06:51:05,789 INFO      PUT http://rkt-elasticsearch:9200/action_history/_create/action20211204120000.yaml [status:201 request:0.007s]
2021-12-08 06:51:05,795 INFO      - Executing [./samples/actions//action20211204120000.yaml](/tmp/tmphbgvu5a6)
2021-12-08 06:51:05,858 INFO      Preparing Action ID: 1, "delete_indices"
2021-12-08 06:51:05,859 INFO      Creating client object and testing connection
2021-12-08 06:51:05,862 INFO      Instantiating client object
2021-12-08 06:51:05,867 INFO      Testing client connectivity
..........
2021-12-08 06:51:15,702 INFO      Updating aliases...
2021-12-08 06:51:15,703 INFO      Alias actions: {'actions': [{'remove': {'index': 'test_sample_index_001', 'alias': 'test_sample_index'}}, {'add': {'index': 'test_sample_index_002', 'alias': 'test_sample_index'}}]}
2021-12-08 06:51:15,744 INFO      Action ID: 3, "alias" completed.
2021-12-08 06:51:15,745 INFO      Job completed.
```
and then again
```
$ ES_INDEX_PREFIX=test_ curatorMigrations \
	--elasticsearch-host=rkt-elasticsearch\
	--action-files-path=./samples/actions/\
	--config-file=samples/curator.yml

2021-12-08 06:53:54,797 INFO      GET http://rkt-elasticsearch:9200/ [status:200 request:0.003s]
2021-12-08 06:53:54,800 INFO      PUT http://rkt-elasticsearch:9200/action_history [status:400 request:0.002s]
2021-12-08 06:53:54,804 INFO      POST http://rkt-elasticsearch:9200/action_history/_refresh [status:200 request:0.004s]
2021-12-08 06:53:54,808 INFO      GET http://rkt-elasticsearch:9200/action_history/_doc/action20211204120000.yaml [status:200 request:0.001s]
2021-12-08 06:53:54,808 INFO      - Already executed [action20211204120000.yaml]
2021-12-08 06:53:54,813 INFO      GET http://rkt-elasticsearch:9200/action_history/_doc/action20211204120001.yaml [status:200 request:0.004s]
2021-12-08 06:53:54,813 INFO      - Already executed [action20211204120001.yaml]
```

## Develop
```
docker run -it --network=xxxxxx -v $PWD:/app -w /app python bash
```

```
make test
```
