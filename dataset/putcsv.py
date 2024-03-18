import csv
import sys

def append_csv(csvfile, repo):
    file_obj = open(csvfile, 'a')
    csvwriter = csv.writer(file_obj)
    mlist = []
    txt_obj = open(repo, 'r')
    lines = txt_obj.readlines()
    for line in lines:
        mlist.append(line[1])
    csvwriter.writerows(mlist)

    txt_obj.close()
    file_obj.close()

csvfile = './expRQ2_results/sheet.csv'
repo = sys.argv[1]

append_csv(csvfile, repo)

