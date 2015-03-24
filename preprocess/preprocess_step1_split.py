# -*- encode: utf-8 -*-
import sys,csv,time

# =======================
# Preprocess Step 1:
# Author: Zhang Xiaoyang, zhangxy.pro@gmail.com
# Usage: python preprocess_step1_split.py adm.csv output_sorted.csv
# Require: spid_media_type.csv
# Drop unnecessary fields
# Translate spid into media and adtype; YMDhrs into readable time_stamp
# split original data into correct sorted and error sorted files
# =======================

LINE_LIMIT = 100000 # Maximun linenum for each file
src_file = sys.argv[1]
dest_file = sys.argv[2]
spid_file = 'spid_media_type.csv'
conv_file = 'adm_conversion.csv'
error_sort_file = 'error_sort_file.csv'

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

def process_line(line):
    mzid = line[0]
    cid = line[2]
    spid = line[3]
    try:
        media = spid_dict[spid][0]
        adtype = spid_dict[spid][1]
    except:
        print "no spid in dict!"
        media,adtype = "",""
    br = line[4]
    os = line[5]
    # lan = line[10]
    time_stamp = decode_time(line[-2])
    isClick = line[-1]
    isCVR = '0'
    if (conv_dict.has_key(mzid)) and (time_stamp in conv_dict[mzid]):
        print "conversion record!"
        time.sleep(5)
        isCVR = '1'
    return [mzid,cid,spid,media,adtype,br,os,time_stamp,isClick,isCVR]

# mzid,cid,spid,media,adtype,br,os,time_stamp,isClick,isCVR
if __name__ == '__main__':
    print "start time: %s" % time.clock()
    spid_dict = {}
    spid_reader = csv.reader(open(spid_file,'r'),delimiter = '^')
    for spid_line in spid_reader:
        spid = spid_line[0]
        media = spid_line[1]
        adtype = spid_line[2]
        spid_dict[spid] = [media,adtype]
    print "spid_dict complete"
    conv_dict = {}
    conv_reader = csv.reader(open(conv_file,'r'),delimiter = ' ')
    for conv_line in conv_reader:
        conv_mzid = conv_line[0]
        conv_time = conv_line[1]
        if conv_dict.has_key(conv_mzid):
            conv_dict[conv_mzid].append(conv_time)
        else:
            conv_dict[conv_mzid] = [conv_time]
    print "conv_dict complete"
    spid = None
    cnt = 0
    cntErrorSort = 0
    correct_mzid_num = 0
    last_mzid_num = 0
    with open(src_file,'r+') as f:
        reader = csv.reader(f,delimiter = '^')
        writer = csv.writer(file(dest_file,'w'),delimiter = ',')
        error_writer = csv.writer(file(error_sort_file,'w'),delimiter=',')
        header = ['mzid','cid','spid','media','adtype','br','os','YMHDhms','isClick','isCVR']
        writer.writerow(header)
        error_writer.writerow(header)

        for line in reader:
            cnt += 1
            final_line = process_line(line)
            # judge current line if error sorted
            current_mzid_num = int(final_line[0].replace("m",""))
            if (current_mzid_num - correct_mzid_num < 0) or (current_mzid_num - correct_mzid_num > 1):
                cntErrorSort += 1
                print ("cnt #%d: m%s, error sort #%d: %s") % (cnt,correct_mzid_num,cntErrorSort,final_line[0])
                error_writer.writerow(final_line)
            else:
                correct_mzid_num = current_mzid_num
                writer.writerow(final_line)
            if cnt % 500000 == 0 and cnt > 0:
                print 'cnt: ' + str(cnt)
                print 'ErrorSort cnt: ' + str(cntErrorSort)
                print "Running time: %s" % time.clock()
                time.sleep(1)
                # break
