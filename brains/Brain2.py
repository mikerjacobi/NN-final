import time
import sys
import random
from neuron import *
import plotting as p

class Brain2:
	name='brain2'
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
	constantBR=-.1

	def set_brain(self):
		pass

	def __init__(self):
		#initialize class vars
		self.startTime=time.time()

		#network for moving
		movementNeurons=[]
		movementNeurons.append(Neuron([1],None,1,'front-back','constant',self.constantFB,None))
		movementNeurons.append(Neuron([1],None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron([1],None,1,'body-rotate','constant',self.constantBR,None))
		movementNeurons.append(Neuron([1],None,1,'head-rotate','constant',0,None))
		self.networks.append(movementNeurons)		

		#single eyeball network
		eyeballs=[]
		eta=.1
		threshold=.9
	
		bias=1
		weights=[bias,1,1,1]
		RGB=Neuron(weights,None,eta,'eyeball','step-input',threshold,None)
		eyeballs.append(RGB)
		self.networks.append(eyeballs)

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		#food network v2
		inputVector=[1]+eye[15]
		n=self.networks[1][0]
		n.inputNeurons=inputVector
		n.propagate()
		eat=n.y

		#movement network
		moveNeurons=self.networks[0]
		for n in moveNeurons:
			n.propagate()
		fb=moveNeurons[0].y
		lr=moveNeurons[1].y
		br=moveNeurons[2].y
		hr=moveNeurons[3].y

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
		#eye network; note that this doesn't change the neuron
		self.networks[1][0].updateWeights(dcharge)
	
		#movement network; doesn't change move neurons
		for n in self.networks[0]:
			n.updateWeights(None)
		
		return 1











