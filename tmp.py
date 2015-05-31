import sys
reload(sys)
sys.setdefaultencoding('utf8')

file_name = "sorted.public.adm.log.3.0"
f = open(file_name,"rb")
f_w = open("adm-sorted-100k.csv","wb")

lines = f.readlines(100000)
f.close()
for line in lines:
    f_w.write(line)
f_w.close()
