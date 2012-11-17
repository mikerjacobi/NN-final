import time
import sys
import random
from neuron import *
import plotting as p

class Brain2:
	networks=[]
	survivalDuration=0
	energy=[]
	time=None
	constantFB=.25

	def set_brain(self):
		pass

	def __init__(self):
		#initialize class vars
		self.time=time.time()

		#network for moving
		movementNeurons=[]
		movementNeurons.append(Neuron(None,None,1,'front-back','constant',self.constantFB,None))
		movementNeurons.append(Neuron(None,None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron(None,None,1,'body-rotate','constant',0,None))
		movementNeurons.append(Neuron(None,None,1,'head-rotate','constant',0,None))
		self.networks.append(movementNeurons)		

		#single eyeball network
		eyeballs=[]
		eta=.1
		threshold=.9
	
	
		RGB=Neuron(None,None,eta,'eyeball','step',threshold,None)
		eyeballs.append(RGB)
		self.networks.append(eyeballs)

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		#food network v2
		inputVector=eye[15]
		n=self.network[1][0]
		n.inputNeurons=inputVector
		n.propagate()
		eat=n.y
		print eat


		#movement network
		moveNeurons=self.networks[0]
		for n in moveNeurons:
			n.propagate()
		fb=moveNeurons[0].y
		lr=moveNeurons[1].y
		br=moveNeurons[2].y
		hr=moveNeurons[3].y

		return eat,fb,lr,br,hr	

	def run_brain(self, args):
		pass	
	
	def process_stats(self,data):
		self.survivalDuration+=1
		self.energy.append(data[0])
		

	def reset(self):
		#calculations
		averageEnergy=0.0
		for e in self.energy: averageEnergy+=e
		averageEnergy/=self.survivalDuration

		#record data
		f=open('data/brain2/brain2Data.txt','a')
		f.write('%f, %f, %d, %f\n'%(self.time, averageEnergy, self.survivalDuration, self.constantFB))
		f.close()
		
		#plots
		name='data/brain2/%d-%f-EvT.png'%(int(self.time),self.constantFB)
		p.plotEnergyVsTime(self.energy,name)

		#reset class vars
		self.time=time.time()
		self.energy=[]
		self.survivalDuration=0

	def learn(self,dcharge):
		#food network; note that this doesn't change the neuron
		self.networks[0].updateWeights(None)
	
		#movement network; doesn't change move neurons
		for n in self.networks[1]:
			n.updateWeights(None)
		
		return 1











