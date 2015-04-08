from py_gapbide import *
sdb = [["search1",2,3,4], ["search1",4,2,3,5], ["search1",2,4,3,"search1",2,3,"search1"], ["search1",2,4,3,"search1"], ["search1",3,5], [2,3,4], [2,"search1",5], [3,5,3,"search1"], [2,4,"search1",5,2,3,3] ]
g = Gapbide(sdb, 3, 0, 5)
g.run()
