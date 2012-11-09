import time
import sys
import random
from neuron import *

class Brain1:
	networks=[]
	def set_brain(self):
		pass

	def __init__(self):
		#network for eating
		n=Neuron(None,None,1,'food neuron','constant',1,None)
		self.networks.append(n)

		#network for moving
		movementNeurons=[]
		movementNeurons.append(Neuron(None,None,1,'front-back','constant',.1,None))
		movementNeurons.append(Neuron(None,None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron(None,None,1,'body-rotate','constant',0,None))
		movementNeurons.append(Neuron(None,None,1,'head-rotate','constant',0,None))
		self.networks.append(movementNeurons)		

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		#food network
		n=self.networks[0]
		n.propagate()
		eat=n.y

		#movement network
		moveNeurons=self.networks[1]
		for n in moveNeurons:
			n.propagate()
		fb=moveNeurons[0].y
		lr=moveNeurons[1].y
		br=moveNeurons[2].y
		hr=moveNeurons[3].y

		return eat,fb,lr,br,hr	

	def run_brain(self, args):
		pass	

	def reset(self):
		pass

	def learn(self,dcharge):
		#food network; note that this doesn't change the neuron
		self.networks[0].updateWeights(None)
	
		#movement network; doesn't change move neurons
		for n in self.networks[1]:
			n.updateWeights(None)
		
		return 1











