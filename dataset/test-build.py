import dataset_api
import sys
import json

file_obj = open('bug_files.json')
data = json.load(file_obj)
test_repo = list(data.keys())
test_repo = test_repo[int(sys.argv[1]):int(sys.argv[2])]
# print(test_repo)
file_obj.close()
# exit()

for repo in test_repo:
    print('Downloading ', repo, '-----\n')
    dataset_api.download_buggy_data_by_repo(repo)
    # print('Testing ', repo, '-----\n')
    # dataset_api.test_default_buggy_codes(repo)
