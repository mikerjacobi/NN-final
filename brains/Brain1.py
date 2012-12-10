import time
import sys
import random
from neuron import *
import plotting as p

class Brain1:
	name='brain1'
	networks=[]
	numTimesteps=0
	healthEaten=0
	neutralEaten=0
	poisonEaten=0
	totalRotation=0
	distanceTraveled=0
	energy=[]
	startTime=0
	constantFB=0
	constantBR=0

	def set_brain(self):
		pass

	def __init__(self):
		#initialize class vars
		self.startTime=time.time()

		#network for eating
		n=Neuron([1],None,1,'food neuron','constant',0,None)
		self.networks.append([n])

		#network for moving
		movementNeurons=[]
		movementNeurons.append(Neuron([1],None,1,'front-back','constant',self.constantFB,None))
		movementNeurons.append(Neuron([1],None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron([1],None,1,'body-rotate','constant',0,None))
		movementNeurons.append(Neuron([1],None,1,'head-rotate','constant',0,None))
		self.networks.append(movementNeurons)		

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		
		#food network
		n=self.networks[0][0]
		n.propagate()
		#eat=n.y
		eat=0

		#movement network
		moveNeurons=self.networks[1]
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
		velocityTest=1
		if velocityTest:
			f=open('data/brain1/velocity2.txt','a')
		else:
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

		self.constantFB+=.01
		self.networks[1][0]=Neuron([1],None,1,'front-back','constant',self.constantFB,None)

	def learn(self,dcharge):
		return 1











