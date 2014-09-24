##grid_list={(1,2):{'tg':None,'tn':None,'class':None,'status':'dense'},(2,2):{'tg':None,'tn':None,'class':None,'status':'sparse'},(1,3):{'tg':None,'tn':None,'class':None,'status':'dense'}}
##n_grid ={(1,2):[(2,2),(1,3)],(2,2):[(1,2),(1,3)], (1,3):[(1,2),(2,2)]}
##cluster = {}
############## D-STREAM for processing real time data #################
################ Forming the initial clusters ###########################
def initial_clustering(grid_list,class_name):
    print "In Initial Clustering ...."
    print 'Clusters before', cluster
    update_den_grids(grid_list)
    print 'Grid_list while initialisation',grid_list
    for grid in grid_list :
        t = grid_list[grid]
        if(g_type(t) =="DENSE"):
            t['label'] = class_name            
            if class_name in cluster:
                cluster[class_name].append(grid)
            else:
                cluster[class_name]= []
                cluster[class_name].append(grid)
                print 'Cluster',class_name, 'created'
                class_name +=1
        else :
            print "No cluster"
            t['label']= 'NO_CLASS'
    cluster1= dict(cluster)
    for c in cluster1:
        for g in cluster1[c]:
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
                        print "Moving grid",hkey,"to cluster", c
                        h['label']= c
                        cluster[c].append(hkey)
                        print "Now class of", hkey,"is",h['label']
    plot_cluster()
    return class_name

################ Finding the type of grid(dense,sparse or transitional) ############    
def g_type(value) :
    D = value['density']
    if ( D <= dl ) :
        gtype = "SPARSE"
    elif ( D >= dm ) :
        gtype = "DENSE"
    elif (( D <= dm ) and ( D >= dl )) :
        gtype = "TRANSITIONAL"
    return gtype

############## Updating the density of grids #####################
def update_den_grids(grid_list):
    for grid in grid_list :
        update_charvec(grid,0)

############## Checking if the grid is an outside grid #####################                     
def isoutside(g,ckey):
    for ng in neigh_grid(g):
        if ng not in ckey:
            return True
        
############# Moving a grid from one cluster to another #####################        
def move(c1, c):
    for key in cluster[c1]:
        print "Moving grid",key,"to cluster",c,"from cluster",c1 
        value = grid_list[key]
        value['label']= c
        cluster[c].append(key)
        temp = c1
        del cluster[c1]
        cluster[temp] = []

########### Reading the records from file to a list #################    
def get_den_grid(rec):
    temp1 = float(rec[0])
    temp2 = float(rec[1])
    key= (int(temp2/grid_size[1]), int(temp1/grid_size[0]))
    if key not in grid_list :
        grid_list[key]= {'tg':0,'tm':0, 'density':0,'status':'NORMAL'}                                              ##   adds key to the grid with empty values
        tgrid_list[key]= [rec]
    else :
        tgrid_list[key].append(rec)
    return key

############### Updating the characterstic vector #######################
def update_charvec(g,d):
    vector = grid_list[g]
    vector['tg']= t
    vector['density']= update_den(g,d)

############### Updating the density of grids ###################    
def update_den(g,den):
    d = t - tc
    prev_vect= grid_list[g]
    prev_den = prev_vect['density']
    grid_den = prev_den * float(math.pow(delta,d))+den
    return grid_den

############## Updating the density of grids in before adjust clustering #####################
def update_grids(grid_list,class_name) :
    for grid in grid_list :
        vector = grid_list[grid]
        update_charvec(grid,0)
        if(g_type(vector) == "DENSE"):
            l = vector.setdefault('label',class_name)
            if l == class_name :
                cluster[class_name]= []
                cluster[class_name].append(grid)
                print 'Cluster',class_name, 'created'
                class_name +=1
        else:
            l= vector.setdefault('label','NO_CLASS')

############## Finding the neighbour grids ######################    
def neigh_grid(grid) :
    for j in range(len(grid)):
        temp1= list(grid)
        temp2= list(grid)
        temp1[j] = temp1[j]-1
        temp1 = tuple(temp1)
        temp2[j] = temp2[j]+1
        temp2 = tuple(temp2)
        n_grid = []
        if temp1 in grid_list: 
            n_grid.append(temp1)
        if temp2 in grid_list :
            n_grid.append(temp2)
    return n_grid

################# Removing the SPORADIC grids ########################
def clean_grid(grid_list):
    print 'Cleaning the grid_list'
    beta = 0.3
    gkeys = grid_list.keys()
    for key in list(gkeys):
        value = grid_list[key]
        tg = value['tg']
        ct = t
        tm = value['tm']
        diff = ct-tg
        pi = (cl*(1-math.pow(delta,(diff+1))))/(N*(1-delta))
        if ((value['density'] < pi) and (t >= (1 + beta)*tm)):
            status = value['status']
            if status == 'SPORADIC' :
                temp = key
                grid_list[temp] = []
                del grid_list[key]
                value['tg'] = 0
                value['tm'] = t
                value['density'] = 0
                value['status'] = "NORMAL"
            elif status == 'NORMAL' :
                value['status'] = "SPORADIC"
        else :
            value['status'] = "NORMAL"

################## Getting the maximum size grid ##################
def max_size_cluster(n_grid,cluster):
    max_len = 0
    max_cluster_grid = None
    for key in n_grid :
        ch = get_cluster(key)
        if ch == None :
            print "Key has no cluster yet"
        else:
            size = len(cluster[ch])
            if size > max_len :
                max_len = size
                max_cluster_grid = key
    return max_cluster_grid

#################### Getting the cluster in which the grid exists ###################
def get_cluster(g) :
    key = grid_list[g].setdefault('label','NO_CLASS')
    if key!= 'NO_CLASS':
        return key
    else :
        return None

########## Checking for unconnected clusters and resolving it ##################         
def resolve_connectivity(ckey,class_name):
    print "Checking for unconnected clusters...."
    c2=list()
    for grid in cluster[ckey] :                                                         #checking unconnection
        value = grid_list[grid]
        if g_type(value) is "SPARSE":
            c2 = cluster[ckey]
            c2.remove(grid)
            value['label'] = 'NO_CLASS'
            break
        if isoutside(grid,cluster[ckey]) is False :
            break    
        else :
            for ngrid in neigh_grid(grid):
                if ngrid in cluster[ckey]:
                    break
                else :
                    value = grid_list[ngrid]
                    if g_type(value) is "DENSE" :
                        cluster[class_name]=[]
                        cluster[class_name].append(ngrid)
                        print 'Cluster', class_name,'created'
                        class_name += 1

################ Adjusting the clusters ##############################
def adjust_cluster(grid_list,class_name):
    print "Adjusting the grids...."
    update_grids(grid_list,class_name)
    for g in grid_list:
        print 'Updatation started'
        print "Grid:",g
        value = grid_list[g]
        tg = value['tg']
        prev_call = t- gaptime
        if prev_call < tg <=t :
            ckey = get_cluster(g)
            if ckey != None :
                c= cluster[ckey]
                if ( g_type(value) is "SPARSE" ) :              ## Checking for SPARSE grid
                        print "Sparse grid"
                        if g not in c :
                            continue 
                        else :
                            c.remove(g)                                              ## delete g from cluster c
                            value['label'] = 'NO_CLASS'
                            resolve_connectivity(ckey,class_name)
                elif ( g_type(value) is "DENSE" ) :                          ## checking for dense grid
                     print "Dense grid"
                     h = max_size_cluster(neigh_grid(g),cluster)
                     if h != None :
                         chkey = get_cluster(h)
                         if chkey != None :
                             hvalue = grid_list[h]
                             ch= cluster[chkey]
                             if (g_type(hvalue) is "DENSE") :
                                 if value['label'] == "NO_CLASS" :
                                     value['label'] = ch
                                 else :
                                     g_cluster = get_cluster(g)
                                     if g_cluster == c :
                                         if len(c) > len(ch):
                                             move(ch,c)
                                         elif len(c) <= len(ch):
                                             move(ckey,chkey)
                             elif (g_type(hvalue) is "TRANSITIONAL") :
                                 ctemp= list(ch)
                                 ctemp.append(g)
                                 if value['label'] == "NO_CLASS" and isoutside(h,ctemp):
                                     value['label'] = chkey                                                           
                                 elif len(c) >= len(ch):                   ##move: move h from cluster ch to c
                                     valueh= grid_list[h]
                                     valueh['label']= ckey
                                     c.append(h)
                                     if h not in ch :
                                         continue
                                     else :
                                         ch.remove(h)
            elif ( g_type(value) is "TRANSITIONAL" ) :
                print "Transitional grid"
                n_grid= neigh_grid(g)
                h = max_size_cluster(n_grid,cluster)
                if h != None :
                    ch= get_cluster(h)
                    if ch != None :
                        ctemp= list(cluster[ch])
                        while(n_grid):
                            n_grid.remove(h)
                            if isoutside(g,ctemp):
                                value= grid_list[g]
                                l = value['label']
                                value['label']= ch
                                if l != 'NO_CLASS':
                                    cluster[c].remove(g)
                                cluster[ch].append(g)                        
                                break
                            h = max_size_cluster(n_grid,cluster)
                            if h != None :
                                ch= get_cluster(h)
                                if ch != None :
                                    ctemp= list(cluster[ch])
                                    ctemp.append(g)                                                             ## find largest c' satisfying that g is an outside grid among neighbouring clusters of g
    plot_cluster()
    return class_name


################### Plotting the clusters #####################
def plot_cluster():
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.title("D-STREAM")
    for key in tgrid_list :
        val = tgrid_list[key]
        i = 0
        for i in range(len(val)):
            plt.plot(val[i][0],val[i][1],'bo')
            i += 1
    clabel = None
    plabel = None
    for ckey in cluster :
        cval = cluster[ckey]
        for key in tgrid_list :
            valp = grid_list[key]
            if 'label' not in valp:
                valp['label'] = "NO_CLASS"
            if key in cval :
                val = tgrid_list[key]
                valp = grid_list[key]
                clabel = valp['label']
                if plabel == None :
                    plabel = clabel
                if clabel == plabel :
                    i = 0
                    for i in range(len(val)):
                        plt.plot(val[i][0],val[i][1],'rD')
                        i += 1
                else :
                    i = 0
                    for i in range(len(val)):
                        plt.plot(val[i][0],val[i][1],'gs')
                        i += 1
                val = tgrid_list[key]
                plt.annotate('c',xy = (float(val[0][0])+1500,float(val[0][1])+1500),xytext = (float(val[0][0])+3000,float(val[0][1])+4500),arrowprops=dict(facecolor='black',shrink=0.02))
                plabel = valp['label']
    plt.show()

############# Plotting the time taken to read a set of records in a dataset ####################
def t_plot() :
    plt.xlabel("No. Of Records")
    plt.ylabel("Time(in microseconds)")
    plt.title("Time Plot")
    count = 0
    ctemp = 0
    rt = datetime.datetime.now()
    print "rt:",rt
    rtt = [0]
    tct = [0]
    for rec in input_list:
        count = count + 1
        if count == ctemp + 50:
            ret = datetime.datetime.now()
            print "ret:",ret
            tpt = ret - rt
            print "tpt:",tpt
            pt = tpt.microseconds
            print "pt:",pt
            ctemp = count
            rt = ret
            print "rt:",rt
            rtt.append(pt)
            tct.append(count)
    print "rtt:",rtt
    print "tct:",tct
    plt.plot(tct,rtt,'r--',marker='o')
    plt.show()
        
               
######### MAIN ###############
############# Importing the required packages ##############                    
import math
import matplotlib.pyplot as plt
import csv
import datetime

############### Initializing the data structures and variables ##############
print "Starting the process to form the clusters...."
N=100
input_list = []
grid_list = {}
tgrid_list = {}
cluster = {}
class_name=1
start_time = datetime.datetime.now()

########### Reading the records from file to a list #################
text_file = open("neast.csv", "r")
reader = csv.reader(text_file,delimiter = " ")
for row in reader :
    input_list.append(row)
print "The input data is :"
print input_list

############### Taking the parameters as input from user #################
delta = float(raw_input("Enter the decay factor: "))
cm = float(raw_input("Enter parameter controlling the threshold(1<cm<N): "))
if cm >= N :
    print "Parameter cm is out of range(valid range : 1<cm<N) !!!"
    exit()
cl = float(raw_input("Enter parameter cl (0<cl<1): "))
if cl <= 0 or cl >= 1 :
    print " Parameter cl is out of range(valid range : 0<cl<1) !!!"
    exit()
d1 = float(((N - cm)/(N-cl)))
d2 = float(cl/cm)
d3 = float(max(d2, d1))
d = float(math.log(d3, delta))
dm = cm/(N*(1 - delta))
dl = cl/(N*(1 - delta))
print 'Delta :', delta
print 'dm :', dm
print 'dl :', dl
gaptime = math.floor(d)
assert gaptime != 0, "Modulo by zero (timediff % gaptime) !!!"
print 'Gaptime :', gaptime
grid_size = [2000,4000]
tc= 0
t =1
for rec in input_list :
    g= get_den_grid(rec)
    d = 6000
    update_charvec(g,d)
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
plot_cluster()
t_plot()
end_time = datetime.datetime.now()
print "Start Time:",start_time
print "End Time:",end_time
run_time = end_time - start_time
print "Runtime:",run_time
print "Ending the process...."
