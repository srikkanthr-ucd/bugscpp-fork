import os
import subprocess

dir_path = './Prompts/'
gemini_path = './gemini.py'
directory = os.fsencode(dir_path)
suffix_id = '-prompt.txt'
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    if filename.endswith(suffix_id): 
        cmd = ['python '+gemini_path, dir_path+filename]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        file_raw = filename[:-len(suffix_id)]
        # print(file_raw)
        out_file = open(file_raw+'-response.txt', 'w')
        out_file.write(process.stdout)
    #     # print(os.path.join(directory, filename))
    #     continue
    # else:
    #     continue
