# Take repo as input
# Generate prompt v/
# Using prompt, get llm output x
# Test llm output

import dataset_api

patch_dir = '../bugscpp/taxonomy/'
proj_dir = './data/'

def getInt(str):
    found_num = False
    ret = 0
    for c in str:
        isDig = c.isdigit()
        if isDig and found_num:
            ret = ret * 10 + int(c)
        elif isDig and (not found_num):
            found_num = True
            ret = ret * 10 + int(c)
        elif found_num:
            break
    return ret


def read_file(file_path):
    file_obj = open(file_path, 'r')
    ret = file_obj.read()
    file_obj.close()
    return ret

def write_file(file_path, file_content):
    file_obj = open(file_path, 'w')
    file_obj.write(file_content)
    file_obj.close()


def extract_error(repo):
    tag = repo.split('-')
    raw_id = tag[1]
    id = '0' * (4 - len(repo[1])) + raw_id
    repo_name = tag[0]
    patch_path = patch_dir + repo_name + '/patch/' + id + '-buggy.patch'
    bugfile_name = ''
    file_obj = open(patch_path, 'r')
    lines = file_obj.readlines()
    line_start, line_end = 0, 0
    countLines = False
    for line in lines:
        if line.startswith('diff'):
            words = line.split(' ')[-1]
            bugfile_name = words[2:][:-1]
        if line.startswith('@@'):
            line_start = getInt(line)
            countLines = True
            continue
        if countLines and line.startswith('--'):
            countLines = False
        if countLines and (not line.startswith('-')):
            line_end += 1
    line_start -= 1
    line_end += line_start 
    file_obj.close()
    bugfile_path = proj_dir + repo_name + '/buggy-' + raw_id + '/' + bugfile_name
    file_obj = open(bugfile_path, 'r')
    lines = file_obj.readlines()
    return [''.join(lines[line_start:line_end]), line_start, line_end, bugfile_path]

def get_prompt(repo):
    prompt_prefix = ''' The following C++ code has a bug. Please identify and fix the bug. 
    Make sure to output the entire code in C++.
    '''
    
    dataset_api.download_buggy_data_by_repo(repo)
    bug = list(dataset_api.get_complete_buggy_codes_by_repo(repo).values())[0]
    code = bug['code']
    prompt = prompt_prefix + '\n```cpp\n' + code + '\n```\n'
    return prompt

def test_output(repo, fixed_code):
    error_details = extract_error(repo)
    bugfile_path = error_details[3]
    print(bugfile_path)

    file_content = read_file(bugfile_path)

    tmp_file = './' + repo + '-tmp.txt'
    write_file(tmp_file, file_content)
    write_file(bugfile_path, fixed_code)

    result = dataset_api.test_default_buggy_codes(repo)
    write_file(bugfile_path, file_content)
    return [result.build_result, result.test_cases_result.pass_rate]


# fixed_file_path = './data/berry/fixed-1/src/be_vm.c'
# file_obj = open(fixed_file_path, 'r')
# fixed_code = file_obj.read()
# file_obj.close()


# test_output('berry-1', fixed_code)
