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
	y=0
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
		elif function=='step' or 'touch' or 'step-input':
			#input neurons is an input vector
			self.threshold=a
		elif function=='eye':	
			pass
		elif function=='linear-input':
			pass
		elif function=='product':
			pass
		elif function=='wta':
			pass
		


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
			for i in range(0,len(self.inputNeurons)):
				v+=self.inputNeurons[i].y*self.weights[i]
			if v>self.threshold: self.y=1
			else: self.y=0
		elif self.function=='step-input':
			for i in range(0,len(self.inputNeurons)):
				v+=self.inputNeurons[i]*self.weights[i]
			if v>self.threshold: self.y=1
			else: self.y=0
		elif self.function=='eye':
			maxIndex=self.inputNeurons.index(max(self.inputNeurons))
			if maxIndex==0: self.y=0
			elif maxIndex==1: self.y=-1
			elif maxIndex==2: self.y=1
			else: self.y=0
		elif self.function=='linear-input': #has an input vector instead of input neurons
			#calculate v
			for i in range(len(self.inputNeurons)):
				v+=self.inputNeurons[i]*self.weights[i]
			self.y=v
		elif self.function=='product':#output is the product of inputs
			v=1
			for IN in self.inputNeurons:
				v*=IN.y
			self.y=v
		elif self.function=='wta':
			#i want to output the max input
			#REDO THIS!!!
			pass
		elif self.function=='sigmoid':
			for i in range(1,len(self.inputNeurons)):
				v+=self.inputNeurons[i]*self.weights[i]
			self.y=math.tanh(2*v)/10
		elif self.function=='touch': # We know when we're touching
			#only activate if contact is made on the "face"
			if self.inputNeurons[1] > self.threshold:
				self.y = 1
			else: self.y = 0
		elif self.function=='and':
			#logical AND of input neuron output
			v=1
			for IN in self.inputNeurons:
				v=v and IN.y
			self.y=v
		elif self.function=='negate':
			v=self.inputNeurons[0]
			if v==1:self.y=0
			elif v==0:self.y=1
		return self.y

   	
	def updateWeights(self,d):
		if self.function=='constant':
			pass
		elif self.function=='step':
			pass
		elif 1==2: #this is perceptron learning...
			scalar=(d-self.y)*self.eta
			inputs=[]
			for IN in self.inputNeurons: inputs.append(IN.y)
			scaledInput=vMult(inputs, scalar)
			self.weights=vAdd(self.weights,scaledInput)
		elif self.function=='sigmoid':
			derivSig = (1 - self.y**2)/(5)
			scalar = (d - self.y) * self.eta * derivSig
			delta = vMult(self.inputNeurons, scalar)
			self.weights = vAdd(self.weights,delta)
		else:
			pass










