import dataset_api
def test_repo(repo):
    dataset_api.download_buggy_data_by_repo(repo)
    result = dataset_api.test_default_buggy_codes(repo)
    print(result.build_result, result.test_cases_result.pass_rate)
    # print(result)

test_repo('berry-2')
