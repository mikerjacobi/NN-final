import math

#vector subtract b from a
def vSubtract(a,b):
    c=[]

    for i in range(len(a)):
        c.append(a[i]-b[i])
    return c

def vAdd(a,b):
    c=[]
    for i in range(len(a)):
        c.append(a[i]+b[i])
    return c

def vMult(a,scalar):
    b=[]
    for i in range(len(a)):
        b.append(a[i]*scalar)
    return b


class Neuron:
	name=None
	inputNeurons=None
	weights=None
	eta=None
	y=None
	delta=None
	bias=None
	deltaW=None
	function=None
	center=None #for gaussian
	sigma=None #for gaussian
	constant=None #for constant neuron
	threshold=None #for step neuron
    
   	
	def __init__(self, weights, inputNeurons, eta,name,function,a,b):
		self.weights = weights
		self.eta=eta
		self.name=name
		self.inputNeurons=inputNeurons
		self.function=function
		if function=='radial':
			self.center=float(a)
			self.sigma=float(b)
		elif function=='constant':
			self.constant=float(a)
		elif function=='step':
			#input neurons is an input vector
			self.threshold=a


    #def __len__(self):
    #    return 9999

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name
   	
	def propagate(self):
		v=0
		if self.function=='input':
			pass
		elif self.function=='linear':
            #calculate v
			for i in range(len(self.inputNeurons)):
				v+=self.inputNeurons[i].y*self.weights[i]
			self.y=v
		elif self.function=='radial':
			r=0 #r is the distance between center and x
			for i in range(len(self.inputNeurons)):
				r+=(self.inputNeurons[i].y-self.center[i])**2
			r=math.sqrt(r)
			self.y=math.exp((-.5)*(r**2)/(self.sigma**2))
		elif self.function=='constant':
			self.y=self.constant
		elif self.function=='step': #inputNeurons is a float array
			for i in range(1,len(self.inputNeurons)):
				v+=self.inputNeurons[i]*self.weights[i]
			if v>self.threshold: self.y=1
			else: self.y=0
		return self.y

   	
	def updateWeights(self,d):
		if self.function=='constant':
			pass
		elif self.function=='step':
			pass
		else: #this is perceptron learning...
			scalar=(d-self.y)*self.eta
			inputs=[]
			for IN in self.inputNeurons: inputs.append(IN.y)
			scaledInput=vMult(inputs, scalar)
			self.weights=vAdd(self.weights,scaledInput)










