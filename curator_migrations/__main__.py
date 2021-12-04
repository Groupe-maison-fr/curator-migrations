import argparse
import os.path
from elasticsearch import Elasticsearch
from .str_to_bool import str_to_bool
from .action_history import define_schema
from .action_runner import run_actions


def parse_main_args():
    parser = argparse.ArgumentParser(description='Run curator actions sequentially as in doctrine migrations')
    parser.add_argument('--elasticsearch-host', default='localhost', type=str, help='elasticsearch host')
    parser.add_argument('--elasticsearch-port', default='9200', type=str, help='elasticsearch port')
    parser.add_argument('--action-files-path', default=(os.getcwd() + '/actionFiles'), type=str,
                        help='path of action files')
    parser.add_argument('--action-history-index-name', default='action_history', type=str,
                        help='index name of actions history')
    parser.add_argument('--force-index-creation', default=False, type=str_to_bool,
                        help='force creation of index of actions history')
    parser.add_argument('--override-running-state', default=False, type=str_to_bool,
                        help='force execution even if history action is in running state')
    parser.add_argument('--config-file', default='~/.curator/curator.yml', type=str,
                        help='curator.yml configuration file')
    parser.add_argument('--dry-run', default=False, type=str_to_bool, help='dry-run')
    return parser.parse_args()


def main() -> None:
    args = parse_main_args()

    elasticsearch_client = Elasticsearch(hosts=['%s:%s' % (args.elasticsearch_host, args.elasticsearch_port)])

    define_schema(
        elasticsearch_client,
        args.action_history_index_name,
        args.force_index_creation
    )

    os.environ['ELASTICSEARCH_HOST'] = args.elasticsearch_host
    os.environ['ELASTICSEARCH_PORT'] = args.elasticsearch_port
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
