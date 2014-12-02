from sets import Set
class MSatScan :
    
    def accuracy(self,evcount,B=0):
        TP = evcount['TP']
        TN = evcount['TN']
        FP =  evcount['FP']
        FN = evcount['FN']        
        self.RI= (TP+TN)/(TP+FP+FN+TN)# Rand Measurement
        self.P= TP/(TP+FP) # precise rate
        P= self.P
        self.R = TP/(TP+FN)# recall rate
        R= self.R
        self.FM= ((B^2+1)*P*R)/(B^2*P+R)# F-measure with weightage of recall as 'B'
        self.JI= TP/(TP+FP+FN)# jackard index 
        self.FM = (TP/(TP+FP))*(TP/(TP+FN))
    def hashing(datain):

        #Summarize the data using using hashing techniques
        output= datain
        return output
    def runSatScan(datain):
        #prepare dataset for SatScan in SatScan format
        # run SatScan
        output= datain
        return output
    def evaluate(self,bench,res):
        # make the confusion matrix to calculate true/false positive and negatives
        total = 20
        evcount = dict()
        evcount['TP']=0
        evcount['TN']=0
        evcount['FP']=0
        evcount['FN']=0
        for k in bench:
            if k in res:
                evcount['TP']+=1
            else :
                evcount['FN']+=1
        clus_bench= Set(bench.keys())
        clus_res= Set(res.keys())
        evcount['FP']= len(clus_res- clus_bench)
        evcount['TN']=total- evcount['FP']-evcount['TP']
        print evcount
        self.accuracy(evcount)
        


    #write code here to read the data into datain
    datain= ""
new = MSatScan()
##benchmark= runSatScan(datain)
##    result= runSatScan(dataout)
benchmark ={(0,0):1,(0,1):1}
result ={(0,1):1}
new.evaluate(benchmark,result)
print "jackard index is",new.JI
print "Precision rate is", new.P
print "Recall rate is ", new.R


