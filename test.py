##grid_list={(1,2):{'tg':None,'tn':None,'class':None,'status':'dense'},(2,2):{'tg':None,'tn':None,'class':None,'status':'sparse'},(1,3):{'tg':None,'tn':None,'class':None,'status':'dense'}}
##n_grid ={(1,2):[(2,2),(1,3)],(2,2):[(1,2),(1,3)], (1,3):[(1,2),(2,2)]}
##cluster = {}
def initial_clustering(grid_list,class_name):
##    class_name = 1
    print 'clusters before', class_name
    update_den_grids(grid_list)
    print 'grid_list while initialisation',grid_list
    for grid in grid_list :
        t = grid_list[grid]
        if(g_type(t) =="DENSE"):
            t['label'] = class_name            
            if class_name in cluster:
                print "yes"
                cluster[class_name].append(grid)
            else:
                print 'new'
                cluster[class_name]= []
                cluster[class_name].append(grid)
                print 'cluster',class_name, 'created'
                class_name +=1
            
        else :
            print "no cluster"
            t['label']= 'NO_CLASS'
    cluster1= dict(cluster)             
    for c in cluster1:
        for g in cluster1[c]:
            print "g=",g
            if(isoutside(g,cluster1[c])):
                for hkey in neigh_grid(g):
                    h= grid_list[hkey]
                    c1= h['label']
                    if (c1!= "NO_CLASS"):
                        if(len(cluster1[c])> len(cluster1[c1])):
                            move(c1,c)
                        else :
                            move(c,c1)
                    elif (g_type(h) == "TRANSITIONAL" ) :
                        move(h,c)
    return class_name
    
def g_type(value) :
    D = value['density']
    if ( D <= dl ) :
        gtype = "SPARSE"
    elif ( D >= dm ) :
        gtype = "DENSE"
    elif (( D <= dm ) and ( D >= dl )) :
        gtype = "TRANSITIONAL"
    return gtype
def update_den_grids(grid_list):
    for grid in grid_list :
        update_charvec(grid,0)
                     
def isoutside(g,c1):
    for ng in neigh_grid(g):               
        if ng not in c1:
            return True
def move(c1, c):
    for key in cluster[c1]:
        value = grid_list[key]
        value['label']= c
    cluster[c1].clear()
    
def get_den_grid(rec):
    temp1= rec[0]
    temp2 = rec[1]
    key= (int(temp2/grid_size[1]), int(temp1/grid_size[0]))
    if key not in grid_list :
        grid_list[key]= {'tg':None,'tm':None, 'density':0,'status':'NORMAL'}        ##   adds key to the grid with empty values
    return key
def update_charvec(g,d):
    vector = grid_list[g]
    vector['tg']= t
    vector['density']= update_den(g,d)
    
def update_den(g,den):
    d = t - tc
    prev_vect= grid_list[g]
    prev_den = prev_vect['density']
    grid_den = prev_den * float(math.pow(delta,d))+den
    return grid_den

def update_grids(grid_list,class_name) :
    for grid in grid_list :
        print "grid :",grid
        update_charvec(grid,0)
        vector = grid_list[grid]
        if(g_type(vector) =="DENSE"):
            l = vector.setdefault('label',class_name)
            if l == class_name :
                cluster[class_name]= []
                cluster[class_name].append(grid)
                print 'cluster',class_name, 'created'
                class_name +=1
        else:
            l= vector.setdefault('label','NO_CLASS')
    
def neigh_grid(grid) :
    for j in range(len(grid)):
        temp1= list(grid)
        print "temp1", temp1
        temp2= list(grid)
        temp1[j] = temp1[j]-1
        temp1 = tuple(temp1)
        print "temp1", temp1
        temp2[j] = temp2[j]+1
        temp2 = tuple(temp2)
        print 'temp2', temp2
        n_grid = []
##
##        flag1 = grid_list.has_key(temp1)
        if temp1 in grid_list: 
            n_grid.append(temp1)
##        flag2 = grid_list.has_key(temp2)
        if temp2 in grid_list :
            n_grid.append(temp2)
    print 'n_grid', n_grid    
    return n_grid
def clean_grid(grid_list):
    print 'Cleaning the grid_list'
    beta = 0.3
    for key in grid_list:
        value = grid_list[key]
        tg = value['tg']
        ct = t
##        t = ct.microsecond
        tm = value['tm']
##        temp = ct - tg
##        diff = temp.microseconds
        diff = ct-tg
        pi = (cl*(1-math.pow(delta,(diff+1))))/(N*(1-delta))
        if ((value['density'] < pi) and (t >= (1 + beta)*tm)):
            status = value['status']
            if status == 'SPORADIC' :
                grid_list[key].clear()
                value['tm'] = t
##                remove_grid(key,n_grid)                                                 ## To update neighbour grid
            elif status == 'NORMAL' :
                value['status'] = "SPORADIC"
        else :
            value['status'] = "NORMAL"

def max_size_cluster(n_grid,cluster):
    i = 0
    max_len = 0
    for key in n_grid :
        ch = get_cluster(key,cluster)
        size = len(cluster[h])
        if size > max_len :
            max_len = size
            grid = h
    return grid
def get_cluster(g) :
    key = grid_list[g].setdefault('lable','NO_CLASS')
    return key
         
def resolve_connectivity(cl,class_name):       
    c2=list()
    for grid in cl :
        #checking unconnection
        if g_type(grid) is 'DENSE':
            if isoutside(grid,cl):
                grid_list[grid]['label']= class_name
                cluster[class_name]=[]
                cluster[class_name].append(grid)
                print 'cluster', class_name,'created'
                class_name += 1
                
        elif g_type(grid) is 'TRANSITIONAL':
            for ngrid in neigh_grid(grid):
                   if ngrid in c1:
                       break
                    
def adjust_cluster(grid_list,class_name):
    update_grids(grid_list,class_name)
    for g in grid_list:
        print 'updatation started'
        value = grid_list[g]
        tg = value['tg']
        prev_call = t- gaptime
        if prev_call < tg <t :
            ckey = get_cluster(g,cluster)
            c= cluster[ckey]
            if ( g_type(g) == "SPARSE" ) :                                                                 ## Checking for SPARSE grid
                    c.remove(g)                                                                          ## delete g from cluster c
                    value['label'] = 'NO_CLASS'
                    resolve_connectivity(ckey,class_name)
            elif ( g_type(g) == "DENSE" ) :                                                                   ## checking for dense grid
                h = max_size_cluster(neigh_grid(g),cluster)
                chkey = get_cluster(h,cluster)
        ##          chvalue = cluster[ch]
##                values = grid_list[h]
##                density = values['density']
                ch= cluster[chkey]
                if label == "NO_CLASS" :
                    value['label'] = ch                                                                   ##change_label: label g as in cluster of h
                elif len(c) > len(ch):
                    move(ch,c)                                                    ## change_label: label of grids in ch as in c
                elif len(c) <= len(ch):
                    move(ckey,chkey)                                                  ##change_label: label of grids in c as in cluster of h
                elif (g_type(h)== "TRANSITIONAL") :
                    ctemp= list(ch)
                    ctemp.append(g)
                    if label == "NO_CLASS" and isoutside(h,ctemp):
                        value['label'] = chkey                                                           ##change_label: label g as in ch
                    elif len(c) >= len(ch):
                        ##move: move h from cluster ch to c
                        valueh= grid_list[h]
                        valueh['label']= ckey
                        ch.remove(h)
                        c.append(h)
            elif ( g_type(g) == "TRANSITIONAL" ) :
                ngrid= neigh_grid(g)
                h = max_size_cluter(ngrid,cluster)
                ch= get_cluster(h,cluster)
                ctemp= list(cluster[h])
                while(ngrid):
                    ngrid.remove(h)
                    if isoutside(g,ctemp):
                        value= grid_list[g]
                        l = value['label']
                        value['label']= ch
                        if l != 'NO_CLASS':
                            cluster[c].remove(g)
                        cluster[ch].append(g)                        
                        break
                    h = max_size_cluter(n_grid,cluster)
                    ch= get_cluster(h,cluster)
                    ctemp= list(cluster[h])
                    ctemp.append(g)                                                             ## find largest c' satisfying that g is an outside grid among neighbouring clusters of g
    return class_name        

                    
import math               
N=100
grid_list = {}
cluster = {}
class_name=1
print "The input data is :"
input_list = [[1,2,1], [2,2,2], [1.5,2.9,3], [2,3,4], [2.5,2.5,5], [2.5,3.0,1], [6,4.2,2], [6,4.7,3], [6.5,5.5,4], [7,4,5], [7,5.2,1], [7.5,4.2,2]]
print input_list
delta = float(raw_input("Enter the decay factor: "))
cm = float(raw_input("Enter parameter controlling the threshold(1<cm<N): "))
cl = float(raw_input("Enter parameter cl (0<cl<1): "))
d1 = float(((N - cm)/(N-cl)))
d2 = float(cl/cm)
d3 = float(max(d2, d1))
d = float(math.log(d3, delta))
dm = cm/(N*(1 - delta))
dl = cl/(N*(1 - delta))
print 'delta', delta
print 'dm', dm
print 'dl', dl
gaptime = math.floor(d)
##gaptime= 10
print 'gaptime', gaptime
grid_size = [1,2]
##tc = datetime.datetime.now()
tc= 0
t =1
for rec in input_list :
##    t= datetime.datetime.now()
    
    g= get_den_grid(rec)
    d=rec[2]
    update_charvec(g,d)
##    neigh_grid(g) ## need to call neigh_grid call after gap time for all grids
    timediff= t-tc
    if timediff == gaptime :
        print 'calling initial clustering'
        class_name = initial_clustering(grid_list,class_name)
        print 'cluster after initialisaiton', cluster
    if (timediff % gaptime)== 0:
        clean_grid(grid_list)
        class_name = adjust_cluster(grid_list,class_name)
        print 'after adjust cluster', cluster
    t +=1
print 'cluster', cluster
print 'grids', grid_list

