python_prefix = "/home/codespace/.python/current/bin/python"
script_path = "../bugscpp/bugscpp.py"

bugs_line_tags = ["single-line", "multi-line"]
error_types_tags = ["invalid-condition", "invalid-format-string", "memory-error"]

taxonomy_path = "../bugscpp/taxonomy/"
data_path = "./data/"


corrected_code = '''opcase(FLIP): {
             bvalue *dst = RA(), *a = RKB();
             if (var_isint(a)) {
                var_setint(dst, -a->v.i);
             } else if (var_isinstance(a)) {
                ins_unop(vm, "~", *RKB());
                var_setint(dst, ~*RKB()->v.i);
             }
             reg = vm->reg;
'''

import dataset_api

def getIntInString(str):
    start = False
    ret = 0
    for c in str:
        is_char = c >= '0' and c <= '9'
        if start and is_char:
            ret = ret * 10 + int(c)
        if (not start) and is_char:
            start = True
            ret = int(c)
        if start and (not is_char):
            break
    return ret

def test_api():
    print(dataset_api.search_repositories_by_tags(dataset_api.bugs_line_tags[0], dataset_api.error_types_tags[0]))

    buggy_repo = 'berry-2'

    # download repo data
    dataset_api.download_buggy_data_by_repo(buggy_repo)
    return

    # get buggy code
    buggy_functions = dataset_api.get_buggy_function_by_repo(buggy_repo)
    print(f'{buggy_repo} buggy_function: {buggy_functions}')
    complete_codes = dataset_api.get_complete_buggy_codes_by_repo(buggy_repo)
    print(f'{buggy_repo} buggy_codes: {complete_codes}')

    # test
    # output initial test result
    print('-' * 20 + 'Initial' + '-' * 20)
    result = dataset_api.test_default_buggy_codes(buggy_repo)
    print('test_result:')
    print(f'{result.repo_name}: ')
    print(f'  build_result: {result.build_result}')
    print(f'  test_cases_result: ')
    print(f'    pass_rate: {result.test_cases_result.pass_rate}')
    print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
    print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')

    print('-' * 20 + 'Fixed' + '-' * 20)
    # fixed_code = ' '
    fixed_code = corrected_code
    result = dataset_api.test_buggy_codes(buggy_repo, fixed_code)
    print('test_result:')
    print(f'{result.repo_name}: ')
    print(f'  build_result: {result.build_result}')
    print(f'  test_cases_result: ')
    print(f'    pass_rate: {result.test_cases_result.pass_rate}')
    print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
    print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')

    
def main():
    test_api()
    # buggy_repo_list = download_data_by_tags(bugs_line_tags[0], error_types_tags[1])
    return
    # buggy_repo_list = ['berry-1', 'berry-2', 'berry-3', 'berry-4', 'berry-5']
    for repo in buggy_repo_list:
        download_data_by_repo(repo)

    # return buggy code(whole code file)
    buggy_codes = get_buggy_codes(buggy_repo_list)
    for key, code in buggy_codes.items():
        new_file = open('./bugs-raw/'+key+'.cpp', 'w')
        new_file.write(code[0])
        new_file.close()

    return

    # build repo
    build_in_batch(buggy_repo_list)
    # test
    test_res = test_in_batch(buggy_repo_list)
    print("origin_res: ", test_res)

    # # get the corrected code from LLM
    # corrected_codes = ''
    # update_buggy_code('berry-5', corrected_codes)
    # # build repo
    # build_in_batch(buggy_repo_list)
    # # test
    # test_res = test_in_batch(buggy_repo_list)
    # print("updated_res: ", test_res)

    # restore buggy file
    # restore_buggy_code('berry-5', buggy_codes['berry-5'][0])


if __name__ == "__main__":
    # from fetch import download_data_by_tags, download_data_by_repo, get_buggy_codes
    # from test import build_in_batch, test_in_batch
    # from update import update_buggy_code, restore_buggy_code

    main()