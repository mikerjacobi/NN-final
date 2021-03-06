import time
import sys
#import random
from neuron import *
#import plotting as p

class Brain3:
	name='brain3'
	networks=[]
	numTimesteps=0
	healthEaten=0
	neutralEaten=0
	poisonEaten=0
	totalRotation=0
	distanceTraveled=0
	energy=[]
	startTime=0
	constantFB=.25
	constantBR=.55

	def set_brain(self):
		pass

	def __init__(self):
		#initialize class vars
		self.startTime=time.time()


		#BRAIN1 network for moving
		movementNeurons=[]
		movementNeurons.append(Neuron([1],None,1,'front-back','constant',self.constantFB,None))
		movementNeurons.append(Neuron([1],None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron([1],None,1,'body-rotate','constant',self.constantBR,None))
		movementNeurons.append(Neuron([1],None,1,'head-rotate','constant',0,None))
		self.networks.append(movementNeurons)		

		#BRAIN2 single eyeball network
		eyeballs=[]
		threshold=.9
		eta=.1
		bias=1
	
		#read in from text file
		f=open('eyecolor.txt','r').read().replace(' ','').split('\n')
		weights=f[-2][1:-1].split(',')
		for i in range(len(weights)):
			weights[i]=float(weights[i])

		RGB=Neuron(weights,None,eta,'eyeball','sigmoid',None,None)
		eyeballs.append(RGB)
		self.networks.append(eyeballs)

		#BRAIN3 network for sensing touch
		touchNeuron=[]
		threshold=0.0
		eta=.1
		bias=1
		weights=[bias,1,1,1,1,1,1]
		touch=Neuron(weights,None,eta,'touch','touch',threshold,None)
		touchNeuron.append(touch)
		self.networks.append(touchNeuron)

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		#movement network
		moveNeurons=self.networks[0]
		for n in moveNeurons:
			n.propagate()
		fb=moveNeurons[0].y
		lr=moveNeurons[1].y
		br=moveNeurons[2].y
		hr=moveNeurons[3].y

		#eyeball network
		inputVector=[1]+eye[15]
		n=self.networks[1][0]
		n.inputNeurons=inputVector
		n.propagate()
		
		#touch network
		touchNeuron=self.networks[2][0]
		touchInput=[1.0]+[touch[0][0], touch[1][0], touch[2][0], touch[3][0], touch[4][0], touch[5][0]]
		touchNeuron.inputNeurons=touchInput
		touchNeuron.propagate()

		eat = touchNeuron.y # The agent will try to eat when it touches something

		return eat,fb,lr,br,hr	

	def process_stats(self,data):
		self.numTimesteps+=1
		self.energy.append(data[0])
		if data[-1]>0:
			if data[1]>0: self.healthEaten+=data[-1]
			elif data[1]<0: self.poisonEaten+=data[-1]
			else: self.neutralEaten+=data[-1]
		self.totalRotation+=abs(data[2][2])#rotation
		self.distanceTraveled+=abs(data[2][0])#distance this timestep
		

	def reset(self):
		#save eyeball-color weights
		f=open('eyecolor.txt','a')
		f.write(str(self.networks[1][0].weights)+'\n')
		f.close()
		
		#calculations
		survivalTime=time.time()-self.startTime
		averageEnergy=0.0
		for e in self.energy: averageEnergy+=e
		averageEnergy/=self.numTimesteps

		#neuron stats
		numNeurons,numConnections,numNetworks=0,0,0
		for network in self.networks:
			numNetworks+=1
			for neuron in network:
				if type(neuron)==tuple:
					numNeurons+=3 #color,intensity,product neurons
					numConnections+=9 #4inputs,3inputs,2inputs respectively^^^
				else:
					numNeurons+=1
					numConnections+=len(neuron.weights)

		#record data
		f=open('data/%s/%sdata.txt'%(self.name,self.name),'a')
		info='%d,%d,%d,%f,%f,%d,%d,%d,%d,%d,%d,%d,%d\n'%(self.startTime,survivalTime,self.numTimesteps,averageEnergy,self.constantFB,self.healthEaten,self.neutralEaten,self.poisonEaten,self.totalRotation,self.distanceTraveled,numConnections,numNeurons,numNetworks)
		f.write(info)
		print info
		f.close()
		#plots
		plotname='data/%s/%d-%f-EvT.png'%(self.name,self.startTime,self.constantFB)
		#p.plotEnergyVsTime(self.energy,plotname)

		#reset class vars
		self.startTime=time.time()
		self.energy=[]
		self.numTimesteps=0
		self.healthEaten,self.poisonEaten,self.neutralEaten=0,0,0
		self.totalRotation,self.distanceTraveled=0,0
	

	def learn(self,dcharge):
	#	print dcharge

		#eye network; note that this doesn't change the neuron
		n=self.networks[1][0]
		#print 'error=',dcharge-n.y
		#print n.inputNeurons
		#print n.weights
		n.updateWeights(dcharge)
			
		
		#movement network; doesn't change move neurons
		for n in self.networks[0]:
			n.updateWeights(None)
		
		return 1











