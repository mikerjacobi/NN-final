import time
import sys
import random
from neuron import *
sys.path.append('./neurons')
import test as t
import plotting as p

class Brain7:
	networks={}
	survivalDuration=0
	numEaten=0
	energy=[]
	time=None
	constantFB=.25
	constantBR=.55

	def set_brain(self):
		pass

	def __init__(self):
		#initialize class vars
		self.time=time.time()

		#network for default motion
		movementNeurons=[]
		fbMovement=Neuron(None,None,1,'front-back','constant',self.constantFB,None)
		movementNeurons.append(fbMovement)
		movementNeurons.append(Neuron(None,None,1,'left-right','constant',0,None))
		movementNeurons.append(Neuron(None,None,1,'body-rotate','constant',self.constantBR,None))
		movementNeurons.append(Neuron(None,None,1,'head-rotate','constant',0,None))
		self.networks['movementNeurons']=movementNeurons

		#multi eyeball network
		eyeballs=[]
		eyeWTA=[]
		bodyRotate=[]
		#these weights were learned in brain3
		#color_weights=[-0.53926540216773977, -0.96230437483509246, 0.81583336266276296, 0.50542877417595056]
		color_weights=[0,-1,1,-.01]
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

		#stop motion on (e>.9 and center eye intensity>1) network
		stopmotionNetwork=[]
		threshold=.9#this is what energy level is being compared to
		stepEnergy=Neuron([1],None,None,'stopmotion-step','step-input',threshold,None)
		stepIntensity=Neuron([1],[eyeballs[15][1]],None,'stopmotion-intensity','step',1,None)#if light intensity > 1return 1; else 0
		stopmotionNetwork.append(stepEnergy)
		constant1=Neuron(None,None,None,'stopmotion-constant1','constant',1,None)
		stopmotionNetwork.append(constant1)
		stopmotionNetwork.append(stepIntensity)
		stopAnd=Neuron(None,[stepEnergy,constant1,stepIntensity],None,'stopmotion-energyboolean','and',None,None) #energy>.9 AND constant0 AND intensity>1
		stopmotionNetwork.append(stopAnd)
		negateNeuron=Neuron(None,None,None,'stopmotion-negate','negate',None,None)
		stopmotionNetwork.append(negateNeuron)
		stopmotionNetwork.append(Neuron(None,[negateNeuron,fbMovement],None,'stopmotion-product','product',None,None))#energy>.9 times movement
		self.networks['stopmotionNetwork']=stopmotionNetwork

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
	
		#eat network
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

		#stop motion on e>.9 network
		stopmotionNetwork=self.networks['stopmotionNetwork']
		stepEnergy=stopmotionNetwork[0]
		constant1Neuron=stopmotionNetwork[1]
		stepIntensity=stopmotionNetwork[2]
		stopAndNeuron=stopmotionNetwork[3]
		negateNeuron=stopmotionNetwork[4]
		stopProductNeuron=stopmotionNetwork[5]
		stepEnergy.inputNeurons=[charge]
		stepEnergy.propagate()
		constant1Neuron.propagate()
		stepIntensity.propagate()
		stopAndNeuron.propagate()
		negateNeuron.inputNeurons=[stopAndNeuron.y]
		negateNeuron.propagate()
		stopProductNeuron.propagate()
		fb=stopProductNeuron.y

		return eat,fb,lr,br,hr	

	def run_brain(self, args):
		pass	
	
	def process_stats(self,data):
		self.survivalDuration+=1
		self.energy.append(data[0])
		self.numEaten+=data[-1]
		

	def reset(self):
		#calculations
		averageEnergy=0.0
		for e in self.energy: averageEnergy+=e
		averageEnergy/=self.survivalDuration
		print 'lived for ',self.survivalDuration,'!!!!'

		#record data
		f=open('data/brain7/brain7Data.txt','a')
		f.write('%f, %f, %d, %f, %d\n'%(self.time, averageEnergy, self.survivalDuration, self.constantFB, self.numEaten))
		f.close()
		
		#plots
		name='data/brain7/%d-%f-EvT.png'%(int(self.time),self.constantFB)
		p.plotEnergyVsTime(self.energy,name)

		#reset class vars
		self.time=time.time()
		self.energy=[]
		self.survivalDuration=0
		self.numEaten=0

	def learn(self,dcharge):
		#print dcharge
		#eye network; note that this doesn't change the neuron
		#eyeballs=self.networks[1]
		#for eyeball in eyeballs:
		#	eyeball[0].updateWeights(dcharge)#color
		#	eyeball[1].updateWeights(dcharge)#intensity 
	
		#movement network; doesn't change move neurons
		#for n in self.networks[0]:
		#	n.updateWeights(None)
		
		return 1











