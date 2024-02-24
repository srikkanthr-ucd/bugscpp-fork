patch_dir = '../bugscpp/taxonomy/'
proj_dir = './data/'

import gemini
import parse_llm_output

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

prompt_prefix = ''' The following c++ code has an error in a single line. Please identify the error and fix it. Ensure to output the entire C++ file.'''

def ensure_lines(str, n):
    go = str.split('\n')
    go = go[:n]
    return '\n'.join(go)

def fixWithLLM(repo):
    bug_location = extract_error(repo)
    code, st, en = bug_location[0], bug_location[1], bug_location[2]
    print(code)
    prompt = prompt_prefix + '\n```cpp\n' + code + '\n```\n'    
    print(prompt)
    llm_response = gemini.query_llm(prompt)
    print(llm_response)
    fixed_code = parse_llm_output.extract_code(llm_response)

    fixed_code = ensure_lines(fixed_code, en - st)

    # print('fixed code : ', '-'*20, '\n', fixed_code)
    file_obj = open(bug_location[3], 'r')
    original_file = file_obj.read()
    file_obj.close()
    file_obj = open('tmp'+repo+'.cpp', 'w')
    file_obj.write(original_file)
    file_obj.close()

    split_file = original_file.split('\n')
    final_code = '\n'.join(split_file[:(st-1)]) + '\n' + fixed_code + '\n' + '\n'.join(split_file[en:])
    file_obj = open(bug_location[3], 'w')
    file_obj.write(final_code)

fixWithLLM('berry-1')