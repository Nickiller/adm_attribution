# -*- encode: utf-8 -*-
import sys,csv,time
import mmap
import random
reload(sys)
sys.setdefaultencoding('utf8')
from step2_converter import *

# =======================
# Preprocess Step 2:
# Author: Zhang Xiaoyang, zhangxy.pro@gmail.com
# Usage: python 1preprocess_step2_conv_seq_lr.py 1(sample_ratio)
# Require: conv_original.csv, seg_data/
# Instructions:
# - sample conv and non-conv mzids
# - convert original records to seq and LR data set
# - set params
# =======================

seed = 120 # random.seed(seed)
if len(sys.argv) == 2:
    sample_ratio = int(sys.argv[1])
else:
    sample_ratio = 1
params_list = [30,10,13] # days_limit,mins_limit,max_length
media_type = ['Ch','Search','Com','Video','Portal','Music','Ad','Social']

seq_file = 'sdb_' + str(sample_ratio) + '.csv'
lr_file = 'lr_' + str(sample_ratio) + '.csv'
conv_file = 'conv_original.csv'
seg_file_base = sys.path[0] + '/seg_data/seg_sorted_'

def get_conv_seq(conv_file):
    with open(conv_file,'r+') as f:
        conv_reader = csv.reader(f,delimiter = ',')
        '''
        Generate mzid_dict: {"mzid":{"is_conv":"1/0","last_time":"","records":[[record]]}}
        '''
        conv_dict = {}
        for line in conv_reader:
            if conv_reader.line_num == 1:
                continue
            mzid = line[0]
            if len(line) == 10:
                # print "current conv mzid:%s" % mzid
                conv_dict[mzid] = {}
                conv_dict[mzid]['is_conv'] = "1"
                conv_dict[mzid]['last_time'] = line[-3]
                conv_dict[mzid]['records'] = []
            else:
                conv_dict[mzid]['records'].append(line)
        print ("Time: %s conv_dict complete! Count:%d") % (time.clock(),len(conv_dict))

    '''
    Generate converted seq
    '''
    mzid = ""
    seq_cnt = 0
    seq_len_sum = 0
    seq_list = []
    lr_list = []
    for mzid in conv_dict:
        conv_dict[mzid]['records'].sort(key = lambda l:l[7])
        if conv_dict[mzid]['records'][0][7] > conv_dict[mzid]['last_time']:
            continue
        conv_converter = mzid_converter(mzid,conv_dict[mzid],params_list)
        conv_seq = conv_converter.get_seq()
        if len(conv_seq) > 2:
            seq_list.append(conv_seq)
            conv_lr = conv_converter.get_lr()
            print conv_seq, conv_lr
            lr_list.append(conv_lr)
            # print lr_list
            seq_cnt += 1
            seq_len_sum += len(conv_seq) - 2
    print ("Time: %s conv_seq complete! Count:%d Avg length: %d") % (time.clock(),seq_cnt,seq_len_sum/seq_cnt)
    return seq_cnt,seq_list,lr_list

def get_non_conv_seq(files_num, sampled_num = 4):
    print "Start to gen non conv seq..."
    seg_file = seg_file_base + str(files_num) + ".csv"
    start = (files_num - 1) * 3800000
    end = files_num * 3800000
    population = xrange(start, end)
    sample_set = set(sorted(random.sample(population, sampled_num)))
    min_mzid = min(sample_set)
    max_mzid = max(sample_set)
    cnt = 0
    nonconv_dict = {}
    last_mzid = ''
    with open(seg_file,'r+b') as f:
        # seg_reader = csv.reader(f, delimiter = ",")
        # for line in seg_reader:
        seg_map = mmap.mmap(f.fileno(), 0, prot=mmap.ACCESS_READ)
        for line in iter(seg_map.readline, ""):
            line = line.replace("\r\n",'').split(',')
            mzid = line[0]
            if mzid == 'mzid': continue
            if int(mzid.replace("m",'')) < min_mzid: continue
            if int(mzid.replace("m",'')) > max_mzid: break
            if int(mzid.replace("m",'')) not in sample_set: continue

            if nonconv_dict.has_key(mzid):
                nonconv_dict[mzid]['records'].append(line)
            else:
                cnt += 1
                if cnt % (sampled_num / 10) == 0:
                    print 'gen mzid:',mzid,'cnt:',cnt,time.clock()
                    # break
                nonconv_dict[mzid] = {}
                nonconv_dict[mzid]['is_conv'] = '0'
                nonconv_dict[mzid]['last_time'] = ''
                nonconv_dict[mzid]['records'] = [line]
            if mzid != last_mzid and cnt > 1:
                nonconv_dict[last_mzid]['records'].sort(key = lambda l:l[7])
                nonconv_dict[last_mzid]['last_time'] = nonconv_dict[last_mzid]['records'][-1][7]
            last_mzid = mzid
    nonconv_dict[last_mzid]['records'].sort(key = lambda l:l[7])
    nonconv_dict[last_mzid]['last_time'] = nonconv_dict[last_mzid]['records'][-1][7]
    print ('Time: %s nonconv_dict finished! cnt_mzid: %d') % (time.clock(),cnt)

    seq_list = []
    lr_list = []
    for mzid in nonconv_dict:
        nonconv_converter = mzid_converter(mzid,nonconv_dict[mzid],params_list)
        nonconv_seq = nonconv_converter.get_seq()
        seq_list.append(nonconv_seq)
        nonconv_lr = nonconv_converter.get_lr()
        lr_list.append(nonconv_lr)
        # print ",".join(nonconv_seq)
    return seq_list,lr_list

# mzid,cid,spid,media,adtype,br,os,time_stamp,isClick,isCVR
if __name__ == '__main__':
    print "start time: %s" % time.clock()
    print "*" * 40
    conv_cnt,conv_seq_list,conv_lr_list = get_conv_seq(conv_file)
    print "*" * 40
    # conv_cnt = 2647
    files_num = random.randint(1,99)
    random.seed(seed)
    files_num = 3
    sampled_num = conv_cnt * sample_ratio
    print 'sampled non-conv num:',sampled_num
    nonconv_seq_list,nonconv_lr_list = get_non_conv_seq(files_num, sampled_num)
    seq_list = conv_seq_list + nonconv_seq_list
    lr_list = conv_lr_list + nonconv_lr_list
    # seq_writer = csv.writer(open(seq_file,'wb'), delimiter = ',')
    # for seq in seq_list:
    #     seq_writer.writerow(seq)
    lr_header = ['mzid','stable24H','stableM'] + ['cnt_imp_' + m for m in media_type] + ['cnt_click_' + m for m in media_type] + ['is_CVR']
    lr_writer = csv.writer(open(lr_file,'wb'), delimiter = ',')
    lr_writer.writerow(lr_header)
    for lr in lr_list:
        lr_writer.writerow(lr)
    print '*' * 40
    print ('Total cnt: %s. Finished!') % len(seq_list)
