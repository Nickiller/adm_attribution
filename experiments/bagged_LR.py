# -*- encode:utf-8 -*-
import sys,csv,os
import numpy as np
from sklearn.linear_model import RandomizedLogisticRegression as RandomLR
from sklearn.cross_validation import StratifiedKFold as SKF

reload(sys)
sys.setdefaultencoding('utf8')

data_file = 'lr_1.csv'
# data_reader = csv.reader(open(data_file,'rb'),delimiter = ',')

# records = []
# for record in data_reader:
#     if data_reader.line_num == 1:
#         header = record
#         continue
#     records.append(records)
# print 'fin'
# data = np.array(records)
# print data

data = np.genfromtxt(data_file, dtype = None, delimiter=',', names=True)
print data[1:10,],type(data)
