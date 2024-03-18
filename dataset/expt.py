import prompt_1
import gemini
import json
from parse_llm_output import extract_code
import sys

file_obj = open('bug_files.json')
data = json.load(file_obj)
test_repo = list(data.keys())
test_repo = test_repo[int(sys.argv[1]):int(sys.argv[2])]
# print(test_repo)
file_obj.close()
# exit()

llms = [('Gemini', gemini.query_llm)]

results = {}
for repo in test_repo:
    prompt = prompt_1.get_prompt(repo)
    for llm in llms:
        llm_response = llm[1](prompt)
        print(llm_response)
        code = extract_code(llm_response)
        res = prompt_1.test_output(repo, code)
        results[llm[0]+'/prompt-1/'+repo] = res
        print(llm[0], 'prompt-1', repo, ' = ', res)

# print(results)
