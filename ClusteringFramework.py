
'''references: http://mahout.apache.org/users/clustering/streaming-k-means.html
                hashing techniques:
                        
'''

class Stream(parentClass):
	def _init(self,data):
		
		if (type(data) is url):
			#read url and write to queue variable inputQueue
		#for other data types
        def online(self): #Parallel implementation
		#online implementation
		#process inputQueue and return to tempQueue
	def offline (self):# Parallel implementation
		#read/remove data from tempQueue and 
		# do offline processing and write to the outputQueue
                map(outputQueue)
	def manage ():
		#As soon as outputQueue is full or (above threshold size) this function should be called 
		#write to the file .(using pickle module)
		
	def validation(self):
		self.DBI=calculateDBI()# Davis Bouldin Indes
		self.DuI= calculateDuI()# Dunn Index
		self.SiC=calculateSiC()# Silhut Coefficient
	def Accuracy(self,benchmark,B=0):
		self.RI= (TP+TN)/(TP+FP+FN+TN)# Rand Measurement
		self.P= TP/(TP+FP) # precise rate
		self.R = TP/(TP+FN)# recall rate
		self.FM= ((B^2+1).P.R)/(B^2.P+R)# F-measure with weightage of recall as 'B'
		self.JI= TP/(TP+FP+FN)# jackard index 
		slef.FM = (TP/(TP+FP)).(TP/(TP+FN))
		
