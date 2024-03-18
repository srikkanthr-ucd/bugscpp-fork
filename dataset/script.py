from pathlib import Path
import json
import re

target_path_prefix = "../bugscpp/taxonomy/"
bug_files_name = 'bug_files.json'
test_cases_file_name = 'repo_test_cases.json'


def generate_bug_files():
    data = {}
    for repo in Path(target_path_prefix).iterdir():
        if repo.is_dir() and '__pycache__' not in repo.name:
            patch_path = str(repo) + '/patch'
            for bug_patch in Path(patch_path).iterdir():
                if '-buggy.patch' in bug_patch.name:
                    files_list = []
                    with open(bug_patch, 'r') as file:
                        for line in file:
                            if '---' in line:
                                next_line = next(file, None)
                                while next_line and 'changed' not in next_line:
                                    buggy_file = next_line.strip().split('|')[0].strip()
                                    files_list.append(buggy_file)
                                    next_line = next(file, None)
                                    # print(repo.name + '/' + buggy_file)
                                break  # Exit the loop after finding the first "---"
                    match = re.search(r'[1-9]\d*', bug_patch.name)
                    number = match.group(0) if match else None
                    data[repo.name + '-' + number] = files_list

    with open(bug_files_name, 'w') as file:
        json.dump(data, file, indent=4)


def generate_repo_test_cases_file():
    repo_case_mapping = {}
    for repo in Path(target_path_prefix).iterdir():
        if repo.is_dir() and '__pycache__' not in repo.name:
            metadata_path = str(repo) + '/meta.json'
            with open(metadata_path, 'r') as file:
                data = json.load(file)
                for defect in data['defects']:
                    repo_case_mapping[repo.name + '-' + str(defect['id'])] = defect['case']

    with open(test_cases_file_name, 'a') as file:
        json.dump(repo_case_mapping, file, indent=4)


def generate_repo_tc_failing_info_file():
    repo_tc_failing_info = {}
    repo_list = ['cpp_peglib-4', 'cppcheck-8', 'cppcheck-9', 'cppcheck-11', 'cppcheck-25', 'exiv2-13',
                 'exiv2-15', 'exiv2-20', 'openssl-14', 'openssl-24', 'yara-1', 'yara-2', 'dlt_daemon-1',
                 'yaml_cpp-6', 'ndpi-1', 'libtiff-1', 'libtiff-2', 'libtiff-3', 'libtiff-4', 'libtiff-5',
                 'berry-1', 'berry-2', 'berry-3', 'berry-4', 'berry-5', 'libucl-1', 'libucl-2', 'libucl-3',
                 'libucl-4', 'libucl-5', 'libucl-6']
    with open('./repo_test_cases.json', 'r') as file:
        repo_tcs = json.load(file)
        for repo in repo_list:
            tcs = repo_tcs[repo]
            tc_infos = {}
            for tc in tcs:
                tc_infos[tc] = {'failing_info': '', 'tc_code': ''}
            repo_tc_failing_info[repo] = tc_infos

    with open('repo_tc_failing_info.json', 'w') as file:
        json.dump(repo_tc_failing_info, file, indent=4)


def main():
    # generate_bug_files()
    # generate_repo_test_cases_file()
    generate_repo_tc_failing_info_file()


if __name__ == "__main__":
    main()