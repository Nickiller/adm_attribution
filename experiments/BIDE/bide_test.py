# -*- encode: utf-8 -*-
import sys,csv,time
import random
reload(sys)
sys.setdefaultencoding('utf8')

from bide_gap import *

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
for line in sdb_reader:
    if line[1] == '1':
        cnt_conv += 1
    else:
        cnt_non += 1
    sdb.append(line[2:])
print 'conv:',cnt_conv,'non:',cnt_non,'total:',len(sdb)
likeli_thre = cnt_conv / cnt_non

pdb_file = 'pdb_' + str(cnt_non / cnt_conv) + '.csv'
g = Gapbide(sdb, 500, 0, 0, cnt_conv - 1)
pdb_list = g.run() # [(pattern, sup, likelihood)]
pdb_list.sort(key = lambda l: l[2], reverse = True)
pdb_writer = csv.writer(open(pdb_file,'wb'),delimiter = ';')
pdb_writer.writerow(['pattern','supp','likelihood'])
for line in pdb_list:
    pdb_writer.writerow(line)
print pdb_list

print "*" * 40
print len(pdb_list)
print len(list(p for p in pdb_list if p[2] > likeli_thre))
