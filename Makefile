init:
	pip install -e ".[testing]"

test: init
	python setup.py --verbose test
	python3 -m pylint curator_migrations/ test/
	$(MAKE) end2endTest

end2endTest:
	curl http://elasticsearch:9200/_all -X DELETE
	ELASTICSEARCH_HOST=rkt-elasticsearch \
	ES_INDEX_PREFIX=test_ \
	curatorMigrations \
		--elasticsearch-dsn=http://elasticsearch:9200\
		--action-files-path=./samples/actions/\
		--force-index-creation=false\
		--dry-run=false\
		--config-file=samples/curator.yml\
		--override-running-state=true
