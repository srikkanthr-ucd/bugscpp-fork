import sys 

def extract_code(str):
    response = str.split('\n')

    ell, arr = len(response), -1
    codes = []
    cur_code = ''
    start = False
    for i in range(len(response)):
        if response[i].startswith('```') and start:
            codes.append(cur_code)
            cur_code = ''
            start = False
        if response[i].startswith('```') and (not start):
            start = True
        if start:
            if cur_code != '':
                cur_code += '\n'
            cur_code += response[i]
    if len(codes) > 0:
        return codes[-1]
    else:
        return ''
    
# file_obj = open('berry-1-sol.txt')
# str = file_obj.read()

# print(extract_code(str))
