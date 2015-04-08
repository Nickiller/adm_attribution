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
    def __init__(self, mzid, mzid_list, params_list):
        self.mzid = mzid
        self.mzid_list = mzid_list
        self.param_days_limit = params_list[0] #defines valid days window
        self.param_mins_limit = params_list[1] #same channel in it will be only considered once
        self.param_len_limit = params_list[2]  #control the length of seq
        self.isConv = mzid_list[0][-1]
        self.last_time = conv_time(mzid_list[-1][-3])
        self.seq_list = [mzid,self.isConv]
    def __get_start_time(self):
        if self.param_days_limit <= 0:
            return conv_time("20130101000000")
        else:
            return (self.last_time - datetime.timedelta(days = self.param_days_limit))

    def get_seq(self):
        '''
        Convert to [mzid,isConv,len,chanel1,chanel2...]
        '''
        valid_start_time = self.__get_start_time()
        cur_chl = ""
        cur_chl_time = conv_time("20131201000000")
        for line in self.mzid_list[::-1]:
            if (self.isConv == '1') and (line.index == -1):
                continue
            chl = line[3]
            chl_time = conv_time(line[-3])
            if (chl_time < valid_start_time) or (len(self.seq_list) - 2 > self.param_len_limit):
                # print "violate days or length limit!"
                break
            if (chl == cur_chl) and (chl_time + datetime.timedelta(seconds = self.param_mins_limit * 60) >= cur_chl_time):
                # print "violate mins limit!"
                continue
            elif (chl != cur_chl):
                cur_chl = chl
                cur_chl_time = chl_time
            else:
                print "same chl, long interval!"
            self.seq_list.insert(2,chl)
        return self.seq_list

    def get_lr(self):
        pass
