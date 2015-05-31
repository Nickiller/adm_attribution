# -*- encode: utf-8 -*-
import sys,csv,time
import mmap
import random
reload(sys)
sys.setdefaultencoding('utf8')
from step2_converter import *
from bide_gap import *

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
    sample_ratio = int(raw_input('Please input sample ratio:'))
params_list = [30,10,13] # days_limit,mins_limit,max_length
media_type = ['Ch','Search','Com','Video','Portal','Music','Ad','Social']

seq_file = 'sdb_' + str(sample_ratio) + '.csv'
lr_file = 'lr_' + str(sample_ratio) + '.csv'
all_file = 'all_' + str(sample_ratio) + '.csv'
conv_file = 'conv_original.csv'
seg_file_base = sys.path[0] + '/seg_data/seg_sorted_'

def get_conv_dict(conv_file):
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
    return conv_dict

def get_conv_seq_lr(conv_dict):
    '''
    Generate converted seq
    '''
    mzid = ""
    seq_cnt = 0
    seq_len_sum = 0
    seq_dict = {}
    lr_dict = {}
    for mzid in conv_dict:
        conv_dict[mzid]['records'].sort(key = lambda l:l[7])
        if conv_dict[mzid]['records'][0][7] > conv_dict[mzid]['last_time']:
            continue
        conv_converter = mzid_converter(mzid,conv_dict[mzid],params_list)
        conv_seq = conv_converter.get_seq()
        if len(conv_seq) > 2:
            seq_dict[mzid] = conv_seq
            conv_lr = conv_converter.get_lr()
            print conv_seq, conv_lr
            lr_dict[mzid] = conv_lr
            seq_cnt += 1
            seq_len_sum += len(conv_seq) - 2
    print ("Time: %s conv_seq complete! Count:%d Avg length: %d") % (time.clock(),seq_cnt,seq_len_sum/seq_cnt)
    return seq_cnt,seq_dict,lr_dict

def get_nonconv_dict(files_num, sampled_num = 4):
    print "Sample and generate non conv dict..."
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
    return nonconv_dict

def get_nonconv_seq_lr(nonconv_dict):
    seq_dict = {}
    lr_dict = {}
    for mzid in nonconv_dict:
        nonconv_converter = mzid_converter(mzid,nonconv_dict[mzid],params_list)
        nonconv_seq = nonconv_converter.get_seq()
        seq_dict[mzid] = nonconv_seq
        nonconv_lr = nonconv_converter.get_lr()
        lr_dict[mzid] = nonconv_lr
        # print ",".join(nonconv_seq)
    return seq_dict,lr_dict

def output_dict(conv_dict, nonconv_dict = {}):
    all_writer = csv.writer(open(all_file,'wb'), delimiter = ',')
    all_header = ['mzid','cid','media','adtype','os','stable24H','stable6M','time_stamp','isClick','isCVR']
    all_writer.writerow(all_header)

    for mzid in conv_dict:
        conv_dict[mzid]['records'].sort(key = lambda l:l[7])
        if conv_dict[mzid]['records'][0][7] > conv_dict[mzid]['last_time']:
            continue
        for cline in conv_dict[mzid]['records']:
            if cline[7] <= conv_dict[mzid]['last_time']:
                all_writer.writerow(cline + ['1'])

    for mzid in nonconv_dict:
        all_writer.writerow((nline + ['0']) for nline in nonconv_dict[mzid]['records'])
    print 'dict output complete.'

def output_seq(seq_list):
    print 'start to output seq...'
    seq_writer = csv.writer(open(seq_file,'wb'), delimiter = ',')
    for seq in seq_list:
        seq_writer.writerow(seq)
    print 'seq output complete. Check file:',seq_file

def output_lr(lr_list):
    print 'start to output lr...'
    lr_header = ['mzid','stable24H','stableM'] + ['cnt_imp_' + m for m in media_type] + ['cnt_click_' + m for m in media_type] + ['is_CVR']
    lr_writer = csv.writer(open(lr_file,'wb'), delimiter = ',')
    lr_writer.writerow(lr_header)
    for lr in lr_list:
        lr_writer.writerow(lr)
    print 'lr output complete.Check file:',lr_file

def output_imp_lr(lr_list, lr_imp_file,pdb_feature_list):
    print 'start to out put imp lr...'
    lr_header = ['mzid','stable24H','stableM'] + ['cnt_imp_' + m for m in media_type] + ['cnt_click_' + m for m in media_type] + ['is_CVR'] + pdb_feature_list
    lr_writer = csv.writer(open(lr_imp_file,'wb'),delimiter = ';')
    lr_writer.writerow(lr_header)
    for lr in lr_list:
        lr_writer.writerow(lr)
    print 'imp lr output to file',lr_imp_file

def is_sublist(feature, seq):
    len_f = len(feature)
    len_s = len(seq)
    if len_f > len_s:
        return False
    begin = 0
    end = begin + len_f
    while (end <= len_s):
        if seq[begin:end] == feature:
            return True
        else:
            begin += 1
            end = begin + len_f
    return False

# mzid,cid,spid,media,adtype,br,os,time_stamp,isClick,isCVR
if __name__ == '__main__':
    print "start time: %s" % time.clock()
    print "*" * 40
    conv_dict = get_conv_dict(conv_file)
    conv_cnt,conv_seq_dict,conv_lr_dict = get_conv_seq_lr(conv_dict)

    files_num = random.randint(1,99)
    random.seed(seed)
    files_num = 1
    sampled_num = conv_cnt * sample_ratio
    print 'sampled non-conv num:',sampled_num
    nonconv_dict = get_nonconv_dict(files_num, sampled_num)
    nonconv_seq_dict,nonconv_lr_dict = get_nonconv_seq_lr(nonconv_dict)

    seq_list = conv_seq_dict.values() + nonconv_seq_dict.values()
    lr_list = conv_lr_dict.values() + nonconv_lr_dict.values()
    output_seq(seq_list)
    # output_lr(lr_list)

    print "*" * 40
    mzid_list = conv_seq_dict.keys() + nonconv_seq_dict.keys()
    print len(mzid_list)
    index = range(10) * (len(mzid_list) // 10 + 1)
    random.shuffle(index)
    cv_dict = {}
    '''
    cv_dict: {'0':[m1,m2],'1':[m3,m4]...}
    '''
    for i in range(len(mzid_list)):
        fold = index[i]
        if cv_dict.has_key(fold):
            cv_dict[fold].append(mzid_list[i])
        else:
            cv_dict[fold] = [mzid_list[i]]
    print "split into 10 fold!"

    for fold in range(10):
        print "*" * 40
        print "Generate Fold",fold
        time.sleep(3)
        test_mzid_list = []
        train_mzid_list = []
        test_mzid_list = cv_dict[fold]
        for f in cv_dict.keys():
            if f != fold:
                train_mzid_list += cv_dict[f]
        print len(test_mzid_list),len(train_mzid_list)
        '''
        Get train and test seq list
        '''
        train_seq_list = []
        train_cnt_conv = 0
        for mzid in train_mzid_list:
            if conv_seq_dict.has_key(mzid):
                train_cnt_conv += 1
                train_seq_list.insert(0, conv_seq_dict[mzid])
            else:
                train_seq_list.append(nonconv_seq_dict[mzid])
        print 'Train seq list complete.',len(train_seq_list),'cnt conv:',train_cnt_conv

        test_seq_list = []
        for tmzid in test_mzid_list:
            if conv_seq_dict.has_key(tmzid):
                test_seq_list.insert(0, conv_seq_dict[tmzid])
            else:
                test_seq_list.append(nonconv_seq_dict[tmzid])
        print 'Test seq list complete.', len(test_seq_list)

        '''
        Choose Top 10 pdb feature
        '''
        g = Gapbide([seq[2:] for seq in train_seq_list], 100, 0, 0, train_cnt_conv - 1)
        pdb_list = g.run()
        pdb_list.sort(key = lambda l: l[2], reverse = True)
        pdb_feature_list = [p[0] for p in pdb_list[0:10]]
        print 'Feature chosen:',pdb_feature_list,len(pdb_feature_list)
        '''
        Get pdb feature values vector for train and test
        train_val_dict = {'mzid':[val for feature]}
        '''
        train_val_dict = {}
        test_val_dict = {}
        for f in pdb_feature_list:
            print "test for feature:",f
            for s in train_seq_list:
                if not train_val_dict.has_key(s[0]):
                    train_val_dict[s[0]] = []
                if is_sublist(f,s):
                    train_val_dict[s[0]].append(1)
                else:
                    train_val_dict[s[0]].append(0)

            for ts in test_seq_list:
                if not test_val_dict.has_key(ts[0]):
                    test_val_dict[ts[0]] = []
                if is_sublist(f,ts):
                    test_val_dict[ts[0]].append(1)
                else:
                    test_val_dict[ts[0]].append(0)

        print s,train_val_dict[s[0]]
        print ts,test_val_dict[ts[0]]

        train_lr_list = []
        for mzid in train_val_dict:
            if conv_lr_dict.has_key(mzid):
                train_lr_list.append(conv_lr_dict[mzid] + train_val_dict[mzid])
            else:
                train_lr_list.append(nonconv_lr_dict[mzid] + train_val_dict[mzid])

        test_lr_list = []
        for tmzid in test_val_dict:
            if conv_lr_dict.has_key(tmzid):
                test_lr_list.append(conv_lr_dict[tmzid] + test_val_dict[tmzid])
            else:
                test_lr_list.append(nonconv_lr_dict[tmzid] + test_val_dict[tmzid])

        # if raw_input('Do you want output data into one file? Input 1 to confirm.') == '1':
        #     output_imp_lr(train_lr_list + test_lr_list, 'sample_' + str(sample_ratio) + '_all.csv', pdb_feature_list)
        #     break
        # else:
        print 'Output into seprate files...'
        output_imp_lr(train_lr_list,'sample_' + str(sample_ratio) + '_train_fold_'+ str(fold + 1) +'.csv',pdb_feature_list)
        output_imp_lr(test_lr_list,'sample_' + str(sample_ratio) + '_test_fold_'+ str(fold + 1) +'.csv',pdb_feature_list)
    print "Finished."
