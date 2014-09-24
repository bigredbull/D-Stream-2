############## D-STREAM for processing real time data #################
############## Importing the required packages ###################
from threading import Thread
import time
from Queue import Queue
import math
import datetime
import csv
import matplotlib.pyplot as plt

############### Initializing the data structures and variables ##############
start_time = datetime.datetime.now()
queue = Queue(maxsize = 5)
grid_list = {}
tgrid_list = {}
key = ()
cluster = {}
input_list = []
N=100
class_name=1
t = 1
tc = 0
i = 0
############### Taking the parameters as input from user #################
print "Starting the process to form the clusters...."
delta = float(raw_input("\nEnter the decay factor: "))
cm = float(raw_input("\nEnter parameter controlling the threshold(1<cm<N): "))
if cm >= N :
   print "\nParameter cm is out of range(valid range : 1<cm<N) !!!"
   exit()
cl = float(raw_input("\nEnter parameter cl (0<cl<1): "))
if cl <= 0 or cl >= 1 :
   print "\nParameter cl is out of range(valid range : 0<cl<1) !!!"
   exit()
d1 = float(((N - cm)/(N-cl)))
d2 = float(cl/cm)
d3 = float(max(d2, d1))
d = float(math.log(d3, delta))
dm = cm/(N*(1 - delta))
dl = cl/(N*(1 - delta))
print '\n delta', delta
print '\n dm', dm
print '\n dl', dl
gaptime = math.floor(d)
assert gaptime != 0, "\n Modulo by zero (timediff % gaptime) !!!"
print '\n Gaptime', gaptime

############### Updating the characterstic vector #######################
def update_charvec(g,d):
   print "\ngrid:",g
   vector = grid_list[g]
   print "\nvector:",vector
   vector['tg']= t
   vector['density']= update_den(g,d)
   
############### Updating the density of grids ###################
def update_den(g,den):
    d = t - tc
    prev_vect= grid_list[g]
    prev_den = prev_vect['density']
    grid_den = prev_den * float(math.pow(delta,d))+den
    return grid_den

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


############# Defining the Online Component ####################
    
class OnlineComponent(Thread):
   input_list = []


########### Reading the records from file to a list #################
   text_file = open("neast.csv", "r")
   reader = csv.reader(text_file,delimiter = " ")
   for row in reader :
      input_list.append(row)
   print "\n The input data is :"
   print input_list
   
############# Plotting the time taken to read a set of records in a dataset #############
   print "input_list:",input_list
   plt.xlabel("No. Of Records")
   plt.ylabel("Time(in microseconds)")
   plt.title("Time Plot")
   count = 0
   ctemp = 0
   rt = datetime.datetime.now()
   rtt = [0]
   tct = [0]
   for rec in input_list:
      count = count + 1
      if count == ctemp + 50:
         print "rt:",rt
         ret = datetime.datetime.now()
         print "ret:",ret
         tpt = ret - rt
         print "tpt:",tpt
         pt = tpt.microseconds
         print "pt:",pt
         ctemp = count
         rt = ret
         rtt.append(pt)
         tct.append(count)
   print "rtt:",rtt
   print "tct:",tct
   plt.plot(tct,rtt,'r--',marker='o')
   plt.show()
############ Online Thread ################ 
   def run(self) :
      print "\n Online Component is running !!!"
      grid_size = [2000,4000]
      global queue
      global tc 
      global t
      global i
      
############# Mapping the records to grids #############
      while True :
         rec = OnlineComponent.input_list[i]
         temp1= float(rec[0])
         temp2 = float(rec[1])
         d = 6000
         key= (int(temp2/grid_size[1]), int(temp1/grid_size[0]))
         queue.put(key)
         if key not in grid_list :
            grid_list[key] = {'tg':0,'tm':0, 'density':0,'status':'NORMAL'}             ##   adds key to the grid with empty values
            tgrid_list[key]= [rec]
         else :
            tgrid_list[key].append(rec)
         update_charvec(key,d)
         i += 1
         if i == len(OnlineComponent.input_list):
            print "\n No records in input file !!!"
            return 0

############## Defining the Offline Component ######################
      
class OfflineComponent(Thread):
   def run (self):
      print "\n Offline Component is running !!!"
      
################ Finding the type of grid(dense,sparse or transitional) ##############
      def g_type(value) :
         D = value['density']
         if ( D <= dl ) :
            gtype = "SPARSE"
         elif ( D >= dm ) :
            gtype = "DENSE"
         elif (( D <= dm ) and ( D >= dl )) :
            gtype = "TRANSITIONAL"
         return gtype
      
############## Updating the density of grids before initial clustering  #####################
      def update_den_grids(grid_list):
         klist = []
         klist = grid_list.keys()
         for grid in list(klist) :
            update_charvec(grid,0)

############## Checking if the grid is an outside grid #####################
      def isoutside(g,ckey):
         for ng in neigh_grid(g):
            if ng not in ckey:
               return True
            
############# Moving a grid from one cluster to another #####################
      def move(c1, c):
         for key in cluster[c1]:
            print "\n Moving grid",key,"to cluster",c,"from cluster",c1
            value = grid_list[key]
            value['label']= c
            cluster[c].append(key)
            temp = c1
            del cluster[c1]
            cluster[temp] = []
            
################ Updating the grids before adjust clustering #######################
      def update_grids(grid_list,class_name) :
         gkeys = grid_list.keys()
         for grid in list(gkeys) :
            vector = grid_list[grid]
            update_charvec(grid,0)
            if(g_type(vector) == "DENSE"):
               l = vector.setdefault('label',class_name)
               if l == class_name :
                  cluster[class_name]= []
                  cluster[class_name].append(grid)
                  print 'cluster',class_name, 'created'
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
            print "\n temp1", temp1
            temp2[j] = temp2[j]+1
            temp2 = tuple(temp2)
            print '\n temp2', temp2
            n_grid = []
            if temp1 in grid_list: 
                n_grid.append(temp1)
            if temp2 in grid_list :
                n_grid.append(temp2)
            print '\n n_grid', n_grid    
            return n_grid
         
################# Removing the SPORADIC grids ########################
      def clean_grid(grid_list):
         print '\n Cleaning the grid_list'
         beta = 0.3
         for key in grid_list:
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
                  grid_list[temp] = value
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
         
############### Checking for unconnected clusters and resolving it #########################
      def resolve_connectivity(ckey,class_name):
         print "Checking for unconnected clusters...."
         c2=list()
         for grid in cluster[ckey] :                                                                                       #checking unconnection
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
                        print '\n Cluster', class_name,'created'
                        class_name += 1
                        
################ Forming the initial clusters ###########################
      def initial_clustering(grid_list,class_name):
         print "In Initial Clustering ...."
         print '\n Clusters before', cluster
         update_den_grids(grid_list)
         print '\n Grid_list while initialisation',grid_list
         gkeys = grid_list.keys()
         for grid in list(gkeys) :
            print "\n gl:",grid_list
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
                        print "\n Moving grid",hkey,"to cluster", c
                        h['label']= c
                        cluster[c].append(hkey)
                        print "now class of", hkey,"is",h['label']
         print "\n gl in ini:",grid_list
         plot_cluster()
         return class_name
      
################ Adjusting the clusters ##############################
      def adjust_cluster(grid_list,class_name):
         print "Adjusting the grids...."
         update_grids(grid_list,class_name)
         gkeys = grid_list.keys()
         for g in list(gkeys):
            print '\n Updatation started'
            value = grid_list[g]
            tg = value['tg']
            prev_call = t- gaptime
            if prev_call < tg <=t :
               ckey = get_cluster(g)
               if ckey != None :
                  c= cluster[ckey]
                  if ( g_type(value) is "SPARSE" ) :                                                              ## Checking for SPARSE grid
                     print "\n Sparse grid"
                     if g not in c :
                        continue
                     else :
                        c.remove(g)                                                                             ## delete g from cluster c
                        value['label'] = 'NO_CLASS'
                        resolve_connectivity(ckey,class_name)
                  elif ( g_type(value) is "DENSE" ) :                                                             ## checking for dense grid
                     print "\n Dense grid"
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
                              elif len(c) >= len(ch):                                                        ##move: move h from cluster ch to c
                                 valueh= grid_list[h]
                                 valueh['label']= ckey
                                 c.append(h)
                                 if h not in ch :
                                    continue
                                 else :
                                    ch.remove(h)
                  elif ( g_type(value) is "TRANSITIONAL" ) :
                     print "\n Transitional grid"
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

######### MAIN ###############      
      N=100
      class_name = 1
      while True :
         global t
         global tc
         global queue
         g = queue.get()
         if g in grid_list :
            timediff= t-tc
            if timediff == gaptime :
               print '\n Calling initial clustering'
               class_name = initial_clustering(grid_list,class_name)
               print '\n Cluster after initialisaiton', cluster
            if (timediff % gaptime)== 0:
               clean_grid(grid_list)
               class_name = adjust_cluster(grid_list,class_name)
               print '\n After adjust cluster', cluster
            t += 1
            print '\n Cluster', cluster
            print '\n Grids', grid_list
         else :
            print "\n Grid List is empty"
      
############### Starting the threads ##################
OnlineComponent().start()
OfflineComponent().start()
end_time = datetime.datetime.now()
print "\n ST:",start_time
print "\n ET:",end_time
run_time = end_time - start_time
print "\n Runtime:",run_time
print "Ending the process...."

