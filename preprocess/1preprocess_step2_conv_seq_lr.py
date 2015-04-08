# -*- encode: utf-8 -*-
import sys,csv,time
reload(sys)
sys.setdefaultencoding('utf8')
import os
from step2_converter import *

# =======================
# Preprocess Step 2:
# Author: Zhang Xiaoyang, zhangxy.pro@gmail.com
# Usage: python 1preprocess_step3_conv_seq_lr.py
# Require: spid_media_type.csv,adm_conversion.csv
# Drop unnecessary fields
# Translate spid into media and adtype; YMDhrs into readable time_stamp;
# split original data into correct sorted and error sorted files
# =======================

LINE_LIMIT = 100000 # Maximum line_num for each file
params_list = [0,0,10000] # days_limit,mins_limit,max_length

# mzid,cid,spid,media,adtype,br,os,time_stamp,isClick,isCVR
if __name__ == '__main__':
    print "start time: %s" % time.clock()
    cnt = 0
    src_file = 'split_1.csv'
    with open(src_file,'r+') as f:
        reader = csv.reader(f,delimiter = ',')
        '''
        Building mzid_dict: {"mzid":[[record]]}
        '''
        mzid_dict = {}
        for line in reader:
            cnt += 1
            mzid = line[0]
            if mzid_dict.has_key(mzid):
                mzid_dict[mzid].append(line)
            else:
                mzid_dict[mzid] = [line]
        print ("Time: %s mzid_dict complete!") % (time.clock())

        mzid = ""
        line = ""
        for mzid in mzid_dict:
            if len(mzid_dict[mzid]) == 1:
                seq_list = [mzid, mzid_dict[mzid][0][-1],mzid_dict[mzid][0][3]]
                # print ",".join(seq_list)
                continue
            # print ("Time: %s sort for %s complete!") % (mzid,time.clock())
            mzid_dict[mzid].sort(key = lambda l:l[7])
            converter = mzid_converter(mzid,mzid_dict[mzid],params_list)
            seq_list = converter.get_seq()
            # print ",".join(seq_list)
            # print ("Time: %s for %s complete!") % (mzid,time.clock())
            # break
        print ("Time: %s for %s complete!") % (mzid,time.clock())
