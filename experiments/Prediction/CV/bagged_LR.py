# -*- encode:utf-8 -*-
import sys,csv,os
import numpy as np
from sklearn.linear_model import RandomizedLogisticRegression as RandomLR
# from sklearn.cross_validation import StratifiedKFold as SKF

reload(sys)
sys.setdefaultencoding('utf8')

def getHeader(f):
    header = csv.reader(open(f,'rb'),delimiter = ';').next()
    print header
    return [name.replace("[","").replace("]","").replace("'","").replace(",","").replace(' ','').replace('_','') for name in header[1:]]

for fold in range(1,11):
    train_file = 'sample_1_train_fold_' + str(fold) + '.csv'
    test_file = 'sample_1_test_fold_' + str(fold) + '.csv'
    header = getHeader(train_file)
    print header[18] #isCVR
    train_data = np.genfromtxt(train_file,dtype = 'int', delimiter=';', usecols = set([(i+1) for i in range(29)]),skip_header = 1)
    test_data = np.genfromtxt(test_file,dtype = 'int', delimiter=';', usecols = set([(i+1) for i in range(29)]),skip_header = 1)
    print train_data[1:10,]
    print train_data.shape
    base_train = train_data[:,0:18]
    base_test = test_data[:,0:18]
    print base_test.shape
    base_RLR = RandomLR()
    base_model = base_RLR.fit(base_train[:,0:17],base_train[:,-1])
    print base_model.get_support()

    imp_train = np.hstack((train_data[:,0:17],train_data[:,19:]))
    imp_model = base_RLR.fit(imp_train,base_train[:,-1])
    print imp_model.get_support()
    break
