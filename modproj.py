def get_den_grid(rec):
    flag = "False"
    temp1= rec[0]
    temp2 = rec[1]
    key= (int(temp2/grid_size[1]), int(temp1/grid_size[0]))
    flag = grid_list.has_key(key)
    if flag == "False" :
        grid_list[key].append(None)
    else :
        grid_list.setdefault(key,[])           ##   add key to the grid with empty values
    return key

def update_den(g, value):
    t = datetime.datetime.now()
    d = t - tc
    diff = d.seconds
    grid_den = 0
    grid_den = grid_den + float(math.pow(delta,diff))+value
    return grid_den
    
def update_charvec(g,d):
    grid = grid_list.get(g)
    D = update_den(g,d)
    grid_list[g] = D
##   tg,tm,label,status to be appended to list
    
import math
import datetime
N=3
tc = datetime.datetime.now()
grid_list = {}
key = ()
print "The input data is :"
input_list = [[1,2,1], [2,2,2], [1.5,2.9,3], [2,3,4], [2.5,2.5,5], [2.5,3.0,1], [6,4.2,2], [6,4.7,3], [6.5,5.5,4], [7,4,5], [7,5.2,1], [7.5,4.2,2]]
print input_list
delta = float(raw_input("Enter the decay factor: "))
cm = float(raw_input("Enter parameter controlling the threshold(1<cm<N): "))
cl = float(raw_input("Enter parameter cl (0<cl<1): "))
d1 = float(((N - cm)/(N-cl)))
d2 = float(cl/cm)
d3 = float(max(d2, d1))
d = float(math.log(d3, d1))
gaptime = float(math.floor(d))
grid_size = [2,2]
for rec in input_list :
    t= datetime.datetime.now()
    g= get_den_grid(rec)
    d=rec[2]
    update_charvec(g,d)
    timediff= t-tc
    if timediff.microseconds == gaptime :
        initial_clustering(grid_list)
    if (timediff.microseconds % gaptime)== 0:
        clean_grid(grid_list)
        adjust_cluster(grid_list)
    t= tc
print "grid_list",
print grid_list

def intial_clustering(grid_list):
## update density and assign grid to each cluster 



def clean_grid(grid_list):
##   remove sporadic grid 


def adjust_cluster(grid_list):
##  update density and check for sparse,dense or transitional grid  






        
    
    

    
        
    

