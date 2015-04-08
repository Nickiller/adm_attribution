# -*- encode: utf-8 -*-
import sys,time,datetime
reload(sys)
sys.setdefaultencoding('utf8')
import os
from datetime import datetime as dt
from utils import *

TIME_FORMAT = "%Y%m%d%H%M%S"
class mzid_converter():
    """docstring for mzid_converter"""
    def __init__(self, mzid, mzid_dict, params_list):
        self.mzid = mzid
        self.records = mzid_dict['records']
        self.param_days_limit = params_list[0] #defines valid days window
        self.param_mins_limit = params_list[1] #same channel in it will be only considered once
        self.param_len_limit = params_list[2]  #control the length of seq
        self.last_time = conv_time(mzid_dict['last_time'])
        self.isConv = mzid_dict['is_conv']
        self.seq_list = [mzid,self.isConv]
        self.lr_list = []

    def __get_start_time(self):
        if self.param_days_limit <= 0:
            return conv_time("20130101000000")
        else:
            return (self.last_time - datetime.timedelta(days = self.param_days_limit))

    def validation(self, line, cur_chl, cur_chl_time):
        valid_start_time = self.__get_start_time()
        flag = 0
        chl = line[2]
        chl_time = conv_time(line[-2])

        if (chl_time < valid_start_time) or (len(self.seq_list) - 2 > self.param_len_limit):
            # print "violate days or length limit!"
            flag = -1
            return flag,cur_chl,cur_chl_time

        if (chl == cur_chl) and (chl_time + datetime.timedelta(seconds = self.param_mins_limit * 60) >= cur_chl_time):
            # print "violate mins limit!"
            flag = 1
        else:
            cur_chl = chl
            cur_chl_time = chl_time
        return flag,cur_chl,cur_chl_time

    def get_seq(self):
        '''
        Convert to [mzid,isConv,len,chanel1,chanel2...]
        '''
        valid_start_time = self.__get_start_time()
        cur_chl = ""
        cur_chl_time = conv_time("20131201000000")
        for line in self.records[::-1]:
            flag,cur_chl,cur_chl_time = self.validation(line, cur_chl, cur_chl_time)
            if flag == -1:
                break
            elif flag == 1:
                continue
            else:
                assert flag == 0
                self.seq_list.insert(2,line[2])
        return self.seq_list

    def get_lr(self):
        '''
        convert to LR dataset
        '''
        valid_start_time = self.__get_start_time()
        cur_chl = ""
        cur_chl_time = conv_time("20131201000000")
        media_type = ['Ch','Search','Com','Video','Portal','Music','Ad','Social']
        cnt_imp_val = [0] * 8
        cnt_click_val = [0] * 8
        for line in self.records[::-1]:
            chl = line[2]
            stable_24 = line[5]
            stable_6M = line[6]
            flag,cur_chl,cur_chl_time = self.validation(line, cur_chl, cur_chl_time)
            if flag == 0:
                print 'valid line!',chl,line[-1]
                try:
                    index = [i for i,x in enumerate(media_type) if x in chl][0]
                except:
                    print 'no media class',chl
                    continue
                if line[-1] == '0':
                    cnt_imp_val[index] += 1
                else:
                    assert line[-1] == '1'
                    cnt_click_val[index] += 1
                print 'imp:',cnt_imp_val
                print 'click',cnt_click_val
            elif flag == 1:
                continue
            else:
                assert flag == -1
                break
        self.lr_list = [self.mzid,stable_24,stable_6M] + cnt_imp_val + cnt_click_val + [self.isConv]
        return self.lr_list
