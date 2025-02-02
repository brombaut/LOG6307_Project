import os
import utils
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')

SEARCH_DIR_PATH = "{}/json/package_dependents".format(PROJECT_PATH)
FILE_NAME_SEARCH_STRING = "*.json"
OUTPUT_FILE_PATH = "{}/csv/package_dependents.csv".format(PROJECT_PATH)
OUTPUT_FIELD_NAMES = [
    'repo_name',
    'dependent',
]


def main():
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES)
    print("Finding files to parse that match {} in {}".format(FILE_NAME_SEARCH_STRING, SEARCH_DIR_PATH))
    files_to_parse = utils.get_list_of_unread_files(SEARCH_DIR_PATH, FILE_NAME_SEARCH_STRING)
    print("Found {} files".format(len(files_to_parse)))
    count = 0
    for ftp in files_to_parse:
        try:
            count += 1
            print("{}: Parsing + writing {}".format(count, ftp))
            dependents = utils.load_json_file(ftp)
            repo_name = parse_repo_name_form_file_name(ftp)
            lines_to_write = list()
            for d in dependents:
                lines_to_write.append({
                    'repo_name': repo_name,
                    'dependent': d
                })
            utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES, lines_to_write)
            utils.mark_file_as_read(ftp)
        except Exception as e:
            print("[ERROR] on file {}. Continuing from next file.".format(ftp))
    print("DONE")


def parse_repo_name_form_file_name(json_issue_file_path):
    file_name = os.path.splitext(os.path.basename(json_issue_file_path))[0]
    split_name = file_name.split('@')
    repo_name = f'{split_name[0]}/{split_name[1]}'
    return repo_name


if __name__ == "__main__":
    main()
