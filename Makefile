init:
	pip install -e ".[testing]"
test: init
	python setup.py --verbose test
	python3 -m pylint curator_migrations/ test/
	curl http://rkt-elasticsearch:9200/_all -X DELETE
	ES_INDEX_PREFIX=test_ curatorMigrations \
		--elasticsearch-host=rkt-elasticsearch\
		--action-files-path=./samples/actions/\
		--force-index-creation=false\
		--dry-run=false\
		--config-file=samples/curator.yml\
		--override-running-state=true
