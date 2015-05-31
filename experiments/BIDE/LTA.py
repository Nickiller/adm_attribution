# -*- encode: utf-8 -*-
import sys,csv,time
import random
reload(sys)
sys.setdefaultencoding('utf8')

'''
Author: Zhang Xiaoyang
Mail: zhangxy.pro@gmail.com
Usage:
Instruction: GapBIDE Experiment
'''
if len(sys.argv) == 1:
    sdb_file = 'sdb_1.csv'
else:
    sdb_file = sys.argv[1]
sdb_reader = csv.reader(open(sdb_file,'rb'),delimiter = ',')
sdb = []
cnt_conv = 0
cnt_non = 0
res_dict = {}
for line in sdb_reader:
    if line[1] == '1':
        cnt_conv += 1
        if res_dict.has_key(line[-1]):
            res_dict[line[-1]][0] += 1
        else:
            res_dict[line[-1]] = [1,0]
    else:
        cnt_non += 1
        if res_dict.has_key(line[-1]):
            res_dict[line[-1]][1] += 1
        else:
            res_dict[line[-1]] = [0,1]
lta_file = 'lta_' + str(cnt_non/cnt_conv) + '.csv'
lta_w = csv.writer(open(lta_file,'wb'),delimiter = '\t')
for item in res_dict:
    res_dict[item] = res_dict[item][0] / (res_dict[item][1] * 1.0 + 1)
    lta_w.writerow([item,res_dict[item]])
    print item,res_dict[item]
