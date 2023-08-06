import json
import os
import sys
from pathlib import Path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from testrail_lib.testrail_variables import TESTRAIL_JSON_DATA_FOLDER, TESTRAIL_JSON_DATA_FILENAME
from testrail_lib import TestrailLibrary as tr


THIS_FOLDER = Path(__file__).parent.absolute()
TEMP_FOLDER = Path(THIS_FOLDER).parent / TESTRAIL_JSON_DATA_FOLDER
MAX_ATTACHMENTS = 3


def upload_logs_to_testrail(outputdir):
    json_data_info_file = Path(TEMP_FOLDER) / TESTRAIL_JSON_DATA_FILENAME
    username = os.getenv("TESTRAIL_USERNAME")
    api_key = os.getenv("TESTRAIL_API_KEY")
    testrail = tr.TestrailLibrary(username, api_key)

    if Path(json_data_info_file).exists():
        with open(json_data_info_file) as f:
            json_data_info = json.load(f)
            project_id = json_data_info.get('project_id')
            section_id = json_data_info.get('section_id')
            suite_id = json_data_info.get('suite_id')
            run_id = json_data_info.get('run_id')
            files = os.listdir(outputdir)
            html_files = list(filter(lambda x: x.endswith('.html') and x.startswith('log'), files))
            for log_file in html_files:
                log_path = Path(outputdir) / log_file
                print(f'Adding log file {log_path} to run {run_id}')
                response = testrail.add_attachment_to_run_in_testrail(run_id, log_path)
                if response:
                    print(f'Successfully uploaded file {log_path} to test run {run_id}: {response}')
                else:
                    print(f'Error: {response}')
            attachments = testrail.get_attachments_for_run_in_testrail(run_id)
            attachments_sorted = sorted(attachments, key=lambda x: x.get("created_on"))
            if len(attachments_sorted) > MAX_ATTACHMENTS:
                to_delete = attachments_sorted[0:len(attachments) - MAX_ATTACHMENTS]
                for attachment in to_delete:
                    print(f'Deleting attachment {attachment["name"]} from run {run_id}')
                    try:
                        deleted_response = testrail.delete_attachment_in_testrail(attachment)
                    except Exception as e:
                        print(e)
        os.remove(json_data_info_file)
    else:
        print('No info file found!')


if __name__ == "__main__":
    outputdir = sys.argv[1]
    upload_logs_to_testrail(outputdir)
