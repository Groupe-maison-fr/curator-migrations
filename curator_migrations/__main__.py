import argparse
import os.path
from elasticsearch import Elasticsearch
from .str_to_bool import str_to_bool
from .action_history import define_schema
from .action_runner import run_actions


def parse_main_args():
    parser = argparse.ArgumentParser(description='Run curator actions sequentially as in doctrine migrations')
    parser.add_argument('--elasticsearch-dsn', default='http://localhost:9200/', nargs='+', help='elasticsearch dsn in http://user:password@localhost:9200/')
    parser.add_argument('--elasticsearch-ca-path', default=None, help='elasticsearch certificate authority path')
    parser.add_argument('--action-files-path', default=(os.getcwd() + '/actionFiles'),
                        help='path of action files')
    parser.add_argument('--action-history-index-name', default='action_history',
                        help='index name of actions history')
    parser.add_argument('--force-index-creation', default=False, type=str_to_bool,
                        help='force creation of index of actions history')
    parser.add_argument('--override-running-state', default=False, type=str_to_bool,
                        help='force execution even if history action is in running state')
    parser.add_argument('--config-file', default='~/.curator/curator.yml',
                        help='curator.yml configuration file')
    parser.add_argument('--dry-run', default=False, type=str_to_bool, help='dry-run')
    return parser.parse_args()


def main() -> None:
    args = parse_main_args()

    if args.elasticsearch_ca_path is not None:
        elasticsearch_client = Elasticsearch(
            hosts=args.elasticsearch_dsn,
            use_ssl=True,
            verify_certs=True,
            ca_certs=args.elasticsearch_ca_path
        )
    else:
        elasticsearch_client = Elasticsearch(hosts=args.elasticsearch_dsn)

    define_schema(
        elasticsearch_client,
        args.action_history_index_name,
        args.force_index_creation
    )

    run_actions(
        elasticsearch_client,
        args.action_history_index_name,
        args.config_file,
        args.action_files_path,
        args.override_running_state,
        args.dry_run
    )


if __name__ == "__main__":
    main()
