# -*- coding: utf-8 -*-
import sys,csv,time
reload(sys)
sys.setdefaultencoding('utf8')
import os

# =======================
# Preprocess Step 1:
# Author: Zhang Xiaoyang, zhangxy.pro@gmail.com
# Usage: python preprocess_step1_split.py adm-sorted.csv
# Require: spid_media_type.csv,adm_conversion.csv
# Drop unnecessary fields
# Translate spid into media and adtype; YMDhrs into readable time_stamp;
# split original data into correct sorted and error sorted files
# =======================

NUM_FILES = 1000 # Num of files segmented
MAX_MZID = 380000000
SEG_POINT = MAX_MZID / NUM_FILES
src_file = sys.argv[1]
# spid_file = 'spid_media_type.csv'
spid_file = 'media_cn_en_mapping.csv'
conv_file = 'adm_conversion.csv'
conv_res_file = "conv_original.csv"
base_name = "seg_sorted_"
path = sys.path[0] +'/seg_data/'
print path

def get_spid_dict():
    spid_dict = {}
    spid_reader = csv.reader(open(spid_file,'r'),delimiter = ',')
    for spid_line in spid_reader:
        cn_media = spid_line[0]
        en_media = spid_line[1]
        spid_dict[cn_media] = en_media
    print "spid_dict complete"
    return spid_dict
def get_conv_dict():
    conv_dict = {}
    conv_reader = csv.reader(open(conv_file,'r'),delimiter = ' ')
    conv_flag = 0
    for conv_line in conv_reader:
        conv_mzid = conv_line[0]
        conv_time = conv_line[1]
        if conv_dict.has_key(conv_mzid) and conv_dict[conv_mzid][0] < conv_time: # only consider the earliest conversion
            continue
        else:
            conv_dict[conv_mzid] = [conv_time,conv_flag]
    print "conv_dict complete"
    return conv_dict
def decode_time(timeString):
    codebook = {'+':'00',
                '-':'01',
                '0':'02',
                '1':'03',
                '2':'04',
                '3':'05',
                '4':'06',
                '5':'07',
                '6':'08',
                '7':'09',
                '8':'10',
                '9':'11',
                'A':'12',
                'B':'13',
                'C':'14',
                'D':'15',
                'E':'16',
                'F':'17',
                'G':'18',
                'H':'19',
                'I':'20',
                'J':'21',
                'K':'22',
                'L':'23',
                'M':'24',
                'N':'25',
                'O':'26',
                'P':'27',
                'Q':'28',
                'R':'29',
                'S':'30',
                'T':'31',
                'U':'32',
                'V':'33',
                'W':'34',
                'X':'35',
                'Y':'36',
                'Z':'37',
                'a':'38',
                'b':'39',
                'c':'40',
                'd':'41',
                'e':'42',
                'f':'43',
                'g':'44',
                'h':'45',
                'i':'46',
                'j':'47',
                'k':'48',
                'l':'49',
                'm':'50',
                'n':'51',
                'o':'52',
                'p':'53',
                'q':'54',
                'r':'55',
                's':'56',
                't':'57',
                'u':'58',
                'v':'59',
                'w':'60',
                'x':'61',
                'y':'62',
                'z':'63'
                }
    year = '2013'
    month = codebook[timeString[1]]
    day = codebook[timeString[2]]
    hour = codebook[timeString[3]]
    minute = codebook[timeString[4]]
    sec = codebook[timeString[5]]
    newTimeString = year + month + day + hour + minute +sec
    return newTimeString
def process_line(line,isCVR):
    line[-2] = decode_time(line[-2])
    try:
        line[2] = spid_dict[line[2]]
    except:
        print ("no such cn_media %s") % (line[2])
        line[2] = line[2]
    return line
def gen_conv_line(conv_mzid):
    return [conv_mzid,'','','','','','',conv_dict[conv_mzid][0],'','1']
def write_header(writer):
    header = ['mzid','cid','media','adtype','os','stable24H','stable6M','YMHDhms','isClick','isCVR']
    writer.writerow(header)

# mzid,cid,media,adtype,os,java_6H,java_,time_stamp,isClick,isCVR
if __name__ == '__main__':
    print "start time: %s" % time.clock()
    spid_dict = get_spid_dict()
    conv_dict = get_conv_dict()

    total_cnt = 0
    total_mzid_cnt = 0
    conv_mzid_cnt = 0
    cur_file_num = 0

    with open(src_file,'r+') as f:
        reader = csv.reader(f,delimiter = '^')
        conv_writer = csv.writer(file(conv_res_file,'wb'),delimiter = ',')
        write_header(conv_writer)

        for line in reader:
            cur_mzid = line[0]
            if conv_dict.has_key(cur_mzid):
                final_conv_line = process_line(line,'1')
                if conv_dict[cur_mzid][1] == 0:
                    conv_mzid_cnt += 1 #conv mzid with at least 1 record
                    print ("conv mzid: %s cnt:%d") % (cur_mzid,conv_mzid_cnt)
                    dummy_conv_line = gen_conv_line(cur_mzid) # gen dummy conv line
                    conv_writer.writerow(dummy_conv_line)
                    conv_dict[cur_mzid][1] = 1
                if (line[-3] <= conv_dict[cur_mzid][0]): # write line earlier than conv time into file
                    conv_writer.writerow(final_conv_line)
            else:
                int_mzid = int(cur_mzid.replace('m',''))
                file_num = int(int_mzid / SEG_POINT) + 1
                if file_num > cur_file_num:
                    cur_file_num = file_num
                    cur_file_name = path + base_name + str(cur_file_num) + '.csv'
                    cur_writer = csv.writer(file(cur_file_name,'wb'),delimiter = ',')
                    print ("current mzid: %s output to %s @time %s") % (cur_mzid,cur_file_name,time.clock())
                    write_header(cur_writer)
                final_line = process_line(line,'0')
                cur_writer.writerow(final_line)

        print "Finished. Running time: %s" % time.clock()
