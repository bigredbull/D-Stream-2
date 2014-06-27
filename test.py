grid_list={(1,2):{'tg':None,'tn':None,'class':None,'status':'dense'},(2,2):{'tg':None,'tn':None,'class':None,'status':'sparse'},(1,3):{'tg':None,'tn':None,'class':None,'status':'dense'}}
n_grid ={(1,2):[(2,2),(1,3)],(2,2):[(1,2),(1,3)], (1,3):[(1,2),(2,2)]}
cluster = {}
def initial_clustering (grid_list):
##    update_grids(grid_list)
    class_name = 1
    for grid in grid_list :
        t = grid_list[grid]
        if(t['status'] == 'dense' ):
            t['class'] = class_name
            cluster[class_name]= grid
            class_name +=1
        else :
            t['class']= 'NO_CLASS'
            
    for c in cluster:
        print "c = ", c
        for g in cluster[c]:
            print "cluster", cluster[c]
            print "g=",g
            if(isoutside(g,c)):
                for h in n_grid[g]:
                    c1= h['class']
                    if (h['class']!= "NO_CLASS"):
                        c1= cluster[h['class']]
                        if(len(c)> len(c1)):
                            move(c1,c)
                        else :
                            move(c,c1)
def isoutside(g,c):
    for ng in n_grid[g]:
        if ng not in cluster[c]:
            return true


initial_clustering(grid_list)
print cluster

                    
