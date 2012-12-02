import time
import sys
import random
from neuron import *
import plotting as p

class Brain4:
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


		#BRAIN1 network for moving
		movementNeurons=[]
		movementNeurons.append(Neuron(None,None,1,'front-back','constant',self.constantFB,None))
		movementNeurons.append(Neuron(None,None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron(None,None,1,'body-rotate','constant',.55,None))
		movementNeurons.append(Neuron(None,None,1,'head-rotate','constant',0,None))
		self.networks.append(movementNeurons)		

		#BRAIN4 multi eyeball network
		eyeballs=[]
		eyeWTA=[]
		threshold=.9
		eta=.1
		bias=1
		weights=[bias,1,1,1]

		#for eyeball in eyeballs:
		for i in range(31):
			RGB=Neuron(weights,None,eta,'eyeball-color:'+str(i),'eye',threshold,None)
			intensity=Neuron(weights,None,eta,'eyeball-intensity'+str(i),'linear-input',None,None)
			product=Neuron([1,1],[RGB, intensity] ,eta,'product:'+str(i),'product',None,None)
			eyeballs.append((RGB,intensity,product))
			WTA=Neuron([1], [product], eta, 'WTA:'+str(i), 'linear',None,None)
			eyeWTA.append(WTA)
		for i in range(len(eyeWTA)):
			wta=eyeWTA[i]
			for j in range(len(eyeWTA)):
				if wta!=eyeWTA[j]:
					wta.inputNeurons+=[eyeWTA[j]]
					wta.weights+=[0]
		self.networks.append(eyeballs)
		self.networks.append(eyeWTA)
		lr=Neuron(range(-15,16,1),eyeWTA, eta,'lr-neuron','linear',None,None)
		self.networks.append([lr])

		#BRAIN3 network for sensing touch
		touchNeuron=[]
		threshold=0.0
		eta=.1
		bias=1
		weights=[bias,1,1,1,1,1,1]
		touch=Neuron(weights,None,eta,'touch','step',threshold,None)
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
		eyeballs=self.networks[1]
		for i in range(len(eyeballs)):
			eyeball=eyeballs[i]
			inputVector=[0]+eye[i]
			eyeball[0].inputNeurons=inputVector #this is the color neuron
			eyeball[1].inputNeurons=inputVector #this is the intensity neuron
			eyeball[0].propagate()
			eyeball[1].propagate()
			eyeball[2].propagate()#product neuron

		#eyeball WTA
		eyeWTA=self.networks[2]
		for wta in eyeWTA:
			wta.propagate() #this needs to produce a list of neurons with activations of all zeros with one one.

		#TEST
		maxy=-9999
		maxeye=eyeWTA[0]
		for wta in eyeWTA:
			if wta.y>maxy:
				maxy=wta.y
				maxeye=wta

		for wta in eyeWTA:
			if wta==maxeye: wta.y=1
			else: wta.y=0
        #ENDTEST
		lrNeuron=self.networks[3][0]
		lrNeuron.propagate()
		br=lrNeuron.y
	
		eat=1
		
		#touch network
		touchNeuron=self.networks[4][0]
		touchInput=[1.0]+[touch[0][0], touch[1][0], touch[2][0], touch[3][0], touch[4][0], touch[5][0]]
		touchNeuron.inputNeurons=touchInput
		touchNeuron.propagate()

		return eat,fb,lr,br,hr	

	def run_brain(self, args):
		pass	
	
	def process_stats(self,data):
		self.survivalDuration+=1
		self.energy.append(data[0])
		if self.survivalDuration%1000==0:
			print 'duration:',self.survivalDuration
		

	def reset(self):
		#calculations
		averageEnergy=0.0
		for e in self.energy: averageEnergy+=e
		averageEnergy/=self.survivalDuration
		print 'lived for ',self.survivalDuration,'!!!!'

		#record data
		f=open('data/brain4/brain4Data.txt','a')
		f.write('%f, %f, %d, %f\n'%(self.time, averageEnergy, self.survivalDuration, self.constantFB))
		f.close()
		
		#plots
		name='data/brain4/%d-%f-EvT.png'%(int(self.time),self.constantFB)
		p.plotEnergyVsTime(self.energy,name)

		#reset class vars
		self.time=time.time()
		self.energy=[]
		self.survivalDuration=0

	def learn(self,dcharge):
		#print dcharge
		#eye network; note that this doesn't change the neuron
		eyeballs=self.networks[1]
		for eyeball in eyeballs:
			eyeball[0].updateWeights(dcharge)#color
			eyeball[1].updateWeights(dcharge)#intensity 
	
		#movement network; doesn't change move neurons
		for n in self.networks[0]:
			n.updateWeights(None)
		
		return 1











