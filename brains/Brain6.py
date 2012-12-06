import time
import sys
import random
from neuron import *
sys.path.append('./neurons')
import test as t
import plotting as p

class Brain6:
	name='brain6'
	networks={}
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

		#network for default motion
		movementNeurons=[]
		movementNeurons.append(Neuron([1],None,1,'front-back','constant',self.constantFB,None))
		movementNeurons.append(Neuron([1],None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron([1],None,1,'body-rotate','constant',self.constantBR,None))
		movementNeurons.append(Neuron([1],None,1,'head-rotate','constant',0,None))
		self.networks['movementNeurons']=movementNeurons

		#multi eyeball network
		eyeballs=[]
		eyeWTA=[]
		bodyRotate=[]
		#these weights were learned in brain3
		#color_weights=[-0.53926540216773977, -0.96230437483509246, 0.81583336266276296, 0.50542877417595056]
		color_weights=[0,-1,1,.01]
		intensity_weights=[1,1,1]

		#for eyeball in eyeballs:
		for i in range(31):
			RGB=Neuron(color_weights,None,None,'eyeball-color:'+str(i),'sigmoid',None,None)
			intensity=Neuron(intensity_weights,None,None,'eyeball-intensity'+str(i),'linear-input',None,None)
			product=Neuron([1,1],[RGB, intensity] ,None,'product:'+str(i),'product',None,None)
			eyeballs.append((RGB,intensity,product))
			WTA=Neuron([1], [product], None, 'WTA:'+str(i), 'linear',None,None)
			eyeWTA.append(WTA)

		for i in range(len(eyeWTA)):
			wta=eyeWTA[i]
			for j in range(len(eyeWTA)):
				if wta!=eyeWTA[j]:
					wta.inputNeurons+=[eyeWTA[j]]
					wta.weights+=[0]
		
		self.networks['eyeballs']=eyeballs
		self.networks['eyeWTA']=eyeWTA
		bodyRotate.append(Neuron(range(-15,16,1),eyeWTA, None,'br-neuron','linear',None,None))
		self.networks['bodyRotate']=bodyRotate

		#network for sensing touch and setting an colorintensity threshold on the center eye
		touchNetwork=[]
		touchThreshold=0.0
		bias=1
		weights=[bias,1,1,1,1,1,1]
		touch=Neuron(weights,None,None,'touch','step-input',touchThreshold,None)
		touchNetwork.append(touch)

		ciThreshold=.1
		colorIntensity=Neuron([1],[eyeballs[15][2]],None,'eat-colorintensity','step',ciThreshold,None)
		touchNetwork.append(colorIntensity)
		andTouchNeuron=Neuron([1,1],[touch,colorIntensity],None,'andTouchNeuron','and',None,None)
		touchNetwork.append(andTouchNeuron)
		self.networks['touchNetwork']=touchNetwork

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		#movement network
		moveNeurons=self.networks['movementNeurons']
		for n in moveNeurons: n.propagate()
		fb=moveNeurons[0].y
		lr=moveNeurons[1].y
		br=moveNeurons[2].y
		hr=moveNeurons[3].y

		#eyeball network
		eyeballs=self.networks['eyeballs']
		for i in range(len(eyeballs)):
			eyeball=eyeballs[i]
			color_inputVector=[1]+eye[i]
			intensity_inputVector=eye[i]
			eyeball[0].inputNeurons=color_inputVector #this is the color neuron
			eyeball[1].inputNeurons=intensity_inputVector #this is the intensity neuron
			eyeball[0].propagate()
			eyeball[1].propagate()
			eyeball[2].propagate()#product neuron
		#eyeball WTA
		eyeWTA=self.networks['eyeWTA']
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
		brNeuron=self.networks['bodyRotate'][0]
		brNeuron.propagate()
		br=brNeuron.y
	
		#touch network
		touchNetwork=self.networks['touchNetwork']
		touchNeuron=touchNetwork[0] #neuron associated with touch sensors
		ciNeuron=touchNetwork[1]#color-intensity neuron at the center eye
		andNeuron=touchNetwork[2] #this neuron ands the touchNeuron and ciNeuron
		touchInput=[0.0]+[touch[0][0], touch[1][0], touch[2][0], touch[3][0], touch[4][0], touch[5][0]]
		touchNeuron.inputNeurons=touchInput
		touchNeuron.propagate()
		ciNeuron.propagate()
		andNeuron.propagate()
		eat=andNeuron.y

		return eat,fb,lr,br,hr	

	def run_brain(self, args):
		pass	
	
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
		for network in self.networks.keys():
			numNetworks+=1
			for neuron in self.networks[network]:
				if network=='eyeballs':
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
		return 1











