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
    id=(0,0)
    inputNeurons=[]
    weights=[]
    eta=1
    y=0
    delta=None
    bias=0
    deltaW=0
    function=''
    center=0
    sigma=0
    
    def __init__(self, passedWeights, inputNeurons, eta,id,function,center,sigma):
        self.weights = passedWeights
        self.eta=eta
        self.id=id
        self.inputNeurons=inputNeurons
        self.function=function
        if function=='radial':
            self.center=center
            self.sigma=sigma


    def __len__(self):
        return 9999

    def __repr__(self):
        return '[%s, node%s]'%(str(self.id[0]),str(self.id[1]))

    def __str__(self):
        return '[%s, node%s]'%(str(self.id[0]),str(self.id[1]))

    def propagate(self):
        if self.function=='input':
            pass
        elif self.function=='linear':
            #calculate v
            v=0
            for i in range(len(self.inputNeurons)):
                v+=self.inputNeurons[i].y*self.weights[i]
            self.y=v
        elif self.function=='radial':
            r=0 #r is the distance between center and x
            for i in range(len(self.inputNeurons)):
                r+=(self.inputNeurons[i].y-self.center[i])**2
            r=math.sqrt(r)
            self.y=math.exp((-.5)*(r**2)/(self.sigma**2))
        elif self.function=='bias':
            self.y=1

        return self.y

    def updateWeights(self,d):
        scalar=(d-self.y)*self.eta
        inputs=[]
        for IN in self.inputNeurons: inputs.append(IN.y)
        scaledInput=vMult(inputs, scalar)
        self.weights=vAdd(self.weights,scaledInput)











