# -*- encode: utf-8 -*-
import sys
import csv
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')

f = 'sample_1_all.csv'
dest_f = 'sample_1_ar.csv'
reader = csv.reader(open(f,'rb'),delimiter = ';')
writer = csv.writer(open(dest_f,'wb'),delimiter = ',')

def convert(s):
    if s == '0':
        return '?'
    else:
        return s

for line in reader:
    if reader.line_num == 1:
        header = line[3:19] + [s.replace('[','').replace(']','').replace('\'','').replace(', ','+') for s in line[20:]]
        header.append('class')
        print header
        writer.writerow(header)
        continue
    ar_cvr = line[19]
    ar_line = line[3:19] + [convert(s) for s in line[20:]]
    ar_line.append(ar_cvr)
    writer.writerow(ar_line)
