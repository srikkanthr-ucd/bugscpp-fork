import subprocess
import re
import json
import os
import sys

from pathlib import Path

python_prefix = sys.executable
bugscpp_script_path = "../bugscpp/bugscpp.py"
patch_path_prefix = "../bugscpp/taxonomy/"
target_path = "./data"

search_command_pattern = "{} {} search {} {}"
checkout_fixed_command_pattern = "{} {} checkout {} {} --target {}"
checkout_buggy_command_pattern = "{} {} checkout {} {} --buggy --target {}"


def search_repos(bugs_line_tag, error_types_tag):
    # use subprocess to execute the command and capture the output
    try:
        search_command = search_command_pattern.format(python_prefix, bugscpp_script_path, bugs_line_tag,
                                                       error_types_tag)
        result = subprocess.run(search_command.split(), check=True, text=True, capture_output=True)
        output = result.stdout
        # remove ANSI escape sequences using regular expressions
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        # remove whitespace characters from both ends of a string
        output = output.strip()
        buggy_repo_list = [s.strip() for s in output.split("\n")]
        return buggy_repo_list
    except FileNotFoundError:
        print("Error: The specified file or directory was not found")
    except subprocess.CalledProcessError as e:
        print("Command failed with return code", e.returncode)
        print("Error output:", e.stderr)


def download_data_by_tags(bugs_line_tag, error_types_tag):
    buggy_repo_list = search_repos(bugs_line_tag, error_types_tag)
    for buggy_repo in buggy_repo_list:
        download_data_by_repo(buggy_repo)
    return buggy_repo_list


def download_data_by_repo(buggy_repo):
    try:
        parts = buggy_repo.split("-")
        repo = parts[0]
        index = parts[1]
        if not is_data_exist(repo, index):
            checkout_fixed_command = checkout_fixed_command_pattern.format(python_prefix, bugscpp_script_path, repo,
                                                                           index,
                                                                           target_path)
            checkout_buggy_command = checkout_buggy_command_pattern.format(python_prefix, bugscpp_script_path, repo,
                                                                           index,
                                                                           target_path)
            subprocess.run(checkout_fixed_command.split(), check=True, text=True, capture_output=True)
            subprocess.run(checkout_buggy_command.split(), check=True, text=True, capture_output=True)
        else:
            print("Repo {}-{} already exists".format(repo, index))
    except FileNotFoundError:
        print("Error: The specified file or directory was not found")
    except subprocess.CalledProcessError as e:
        print("Command failed with return code", e.returncode)
        print("Error output:", e.stderr)


def get_buggy_files(buggy_repo):
    with open('bug_files.json', 'r') as file:
        data = json.load(file)
        buggy_files = data.get(buggy_repo)
    return buggy_files


def get_complete_buggy_codes_by_repo(buggy_repo):
    return get_complete_updated_codes(buggy_repo, True)


def get_complete_buggy_codes_in_batch(buggy_repo_list):
    buggy_codes = {}
    with open('bug_files.json', 'r') as f1:
        bug_files = json.load(f1)
        for buggy_repo in buggy_repo_list:
            code_list = {}
            for buggy_file_path in bug_files[buggy_repo]:
                repo, index = buggy_repo.split("-")
                with open(target_path + '/' + repo + '/' + 'buggy-' + index + '/' + buggy_file_path, 'r',
                          encoding='utf-8-sig') as f2:
                    code = f2.read()
                    code_list[os.path.basename(buggy_file_path)] = code
            buggy_codes[buggy_repo] = code_list
    return buggy_codes


def get_complete_fixed_codes_by_repo(buggy_repo):
    return get_complete_updated_codes(buggy_repo, False)


def get_complete_updated_codes(full_repo_name: str, is_buggy: bool):
    code_list = {}
    repo, index = full_repo_name.split("-")
    patch_file_path = patch_path_prefix + repo + '/patch/' + "{:04d}".format(int(index)) + '-buggy.patch'
    changes = parse_patch(patch_file_path)

    for change in changes:
        file_path = change.current_file
        added_lines = change.added_lines
        source_path = target_path + '/' + repo + '/'
        if is_buggy:
            source_path = source_path + 'buggy-' + index + '/' + file_path
        else:
            source_path = source_path + 'fixed-' + index + '/' + file_path
        with open(source_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
            added_lines_indexes = []
            for i, line in enumerate(lines):
                if line.rstrip() in added_lines:
                    added_lines_indexes.append(i + 1)
            file.seek(0)
            code = file.read()
            code_list[os.path.basename(file_path)] = {'code': code, 'buggy_line_no': added_lines_indexes}

    return code_list


def get_buggy_functions(buggy_repo):
    return get_updated_functions(buggy_repo, True)


def get_fixed_functions(repo):
    return get_updated_functions(repo, False)


def get_buggy_functions_in_batch(buggy_repo_list):
    res = {}
    for buggy_repo in buggy_repo_list:
        res[buggy_repo] = get_buggy_functions(buggy_repo)
    return res


def get_updated_functions(full_repo_name: str, is_buggy: bool):
    updated_functions = {}
    repo, index = full_repo_name.split("-")
    patch_file_path = patch_path_prefix + repo + '/patch/' + "{:04d}".format(int(index)) + '-buggy.patch'
    changes = parse_patch(patch_file_path)

    for change in changes:
        file_path = change.current_file
        start_line = change.start_line
        added_lines = change.added_lines
        source_file = target_path + '/' + repo
        if is_buggy:
            source_file = source_file + '/buggy-' + index + '/' + file_path
        else:
            source_file = source_file + '/fixed-' + index + '/' + file_path
        with open(source_file, 'r') as file:
            lines = file.readlines()
            print('reading ', source_file, " has : ", len(lines), ' lines')
            start_index = find_function_start(lines, start_line - 1)
            end_index = find_function_end(lines, start_index)
            function_lines = lines[start_index:end_index + 1]
            added_lines_indexes = []
            for i, line in enumerate(function_lines):
                if line.rstrip() in added_lines:
                    added_lines_indexes.append(i + 1)
            function = "".join(function_lines)
            updated_functions[os.path.basename(file_path)] = {'function': function, 'buggy_line_no': added_lines_indexes}

    return updated_functions


class Change:
    def __init__(self, current_file, start_line, num_lines, added_lines, removed_lines):
        self.current_file = current_file
        self.start_line = start_line
        self.num_lines = num_lines
        self.added_lines = added_lines
        self.removed_lines = removed_lines

    def get_added_lines(self):
        return self.added_lines

    def get_removed_lines(self):
        return self.removed_lines


def parse_patch(patch_file):
    changes = []
    current_file = None  # Used to record the file name currently being parsed

    with open(patch_file, 'r') as file:
        change = None
        for line in file:
            # Find file name
            if line.startswith('diff --git'):
                parts = line.split()
                # Usually the file name is after 'diff --git a/filename b/filename', here we take the 'a/filename' part
                if len(parts) >= 3:
                    current_file = parts[2][2:]  # Remove prefix 'a/'
            # Find rows containing changed information
            elif line.startswith('@@'):
                match = re.search(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', line)
                if match and current_file:
                    start_line = int(match.group(1))
                    num_lines = int(match.group(2))
                    change = Change(current_file, start_line, num_lines, [], [])
                    changes.append(change)
            elif line.startswith('+') and not line.startswith('+++'):
                if change is not None:
                    change.get_added_lines().append(line[1:].rstrip())
            elif line.startswith('-') and not line.startswith('---'):
                if change is not None:
                    change.get_removed_lines().append(line[1:].rstrip())

    return changes


def find_function_start(lines, start_index):
    func_def_regex = re.compile(
        r'^\s*(?:static\s+)?(?:inline\s+)?(?:virtual\s+)?\w+\s+\w+\s*\([^)]*\)\s*(const)?\s*{?\s*$')
    brace_regex = re.compile(r'^\s*\{\s*$')

    print(len(lines), start_index, " ::: debugging")

    for i in range(start_index, -1, -1):
        line = lines[i]
        if func_def_regex.match(line):
            if i + 1 < len(lines) and brace_regex.match(lines[i + 1]):
                return i
            elif i + 1 == len(lines) or lines[i + 1].strip() != '{':
                return i
    return start_index


def find_function_end(lines, start_index):
    open_braces = 0
    found_braces = False

    if lines[start_index].strip() == '{':
        open_braces += 1
        found_braces = True
        start_index += 1

    for i in range(start_index, len(lines)):
        open_braces += lines[i].count('{')
        open_braces -= lines[i].count('}')

        if open_braces == 0 and found_braces:
            return i
        elif open_braces > 0:
            found_braces = True

    return start_index


def is_data_exist(repo, index):
    buggy_path = Path(target_path + "/" + repo + "/buggy-" + index)
    fixed_path = Path(target_path + "/" + repo + "/fixed-" + index)
    return buggy_path.exists() and fixed_path.exists()

