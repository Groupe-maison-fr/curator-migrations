from io import StringIO
import os.path
import logging
import contextlib
import glob
from tempfile import NamedTemporaryFile
import curator
from .action_history import is_action_done, action_start, action_end

logging.basicConfig(format='%(asctime)s %(levelname)-9s %(message)s', level=logging.INFO)


def run_actions(elasticsearch_client, action_history_index_name, curator_config_file, action_files_path,
                override_running_state, dry_run):
    migration_scripts = sorted(map(os.path.basename, glob.glob(action_files_path + '/*.yaml')))

    for migration_script in migration_scripts:
        if is_action_done(elasticsearch_client, action_history_index_name, migration_script, override_running_state):
            logging.info('- Already executed [%s]', migration_script)
            continue
        if dry_run:
            run_action(curator_config_file, '%s/%s' % (action_files_path, migration_script), True)
            continue

        action_start(elasticsearch_client, action_history_index_name, migration_script)
        redirected_output = run_action(curator_config_file, '%s/%s' % (action_files_path, migration_script), False)
        action_end(elasticsearch_client, action_history_index_name, migration_script, redirected_output)


def run_action(curator_config_file, migration_script, dry_run):
    temporary_action_file = template_substitute_environment_variables(migration_script)
    logging.info('- Executing [%s](%s)', migration_script, temporary_action_file)
    redirected_output = StringIO()
    with contextlib.redirect_stdout(redirected_output):
        curator.run(curator_config_file, temporary_action_file, dry_run)

    os.unlink(temporary_action_file)

    return redirected_output.getvalue()


def template_substitute_environment_variables(filename):
    with open(filename, 'r', encoding='UTF-8') as file_descriptor:
        content = file_descriptor.read()
        with NamedTemporaryFile(delete=False, mode='w') as output_file:
            output_file.write(content.format(**os.environ))
            output_file.close()
            return output_file.name
