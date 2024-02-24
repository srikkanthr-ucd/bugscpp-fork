# buggy_repo_list = ['berry-1', 'berry-2', 'berry-3', 'berry-4', 'berry-5']
buggy_repo_list = ['cpp_peglib-8', 'dlt_daemon-1', 'exiv2-20', 'yaml_cpp-6']

def debug_file(filename):
    buggy_code = open(filename+'.cpp', 'r').read()
    prompt = "The following C++ code has an error. Please identify and provide the corrected code.\n" + "```cpp\n" + buggy_code + "\n```\n"
    write_file = open('./Prompts/'+filename+'-prompt.txt', 'w')
    write_file.write(prompt)

for file in buggy_repo_list:
    debug_file(file)
