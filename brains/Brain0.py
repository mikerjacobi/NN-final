import time
import sys
import random
import neuron
sys.path.append('/home/mike/Documents/NN/NN-final/data')
import plotting as p

class Brain0:
	survivalDuration=0
	energy=[]
	time=None

	def set_brain(self):
		pass

	def __init__(self):
		self.time=time.time()

	def run(self,charge,touch,eye,ear0,ear1,actuators,headangle):
		return 0,0,0,0,0

	def run_brain(self, args):
		pass	

	def learn(self,dcharge):
		return 1

	def process_stats(self,data):
		self.survivalDuration+=1
		self.energy.append(data[0])

	def reset(self):
		averageEnergy=0.0
		for e in self.energy:
			averageEnergy+=e
		averageEnergy/=self.survivalDuration

		f=open('data/brain0/brain0Data.txt','a')
		f.write('%f, %f, %d\n'%(self.time,averageEnergy,self.survivalDuration))
		f.close()
		#plotting goes here
		name='data/brain0/%d-EvT.png'%int(self.time)
		p.plotEnergyVsTime(self.energy,name)	

		#reset stats
		self.survivalDuration=0
		self.energy=[]
		self.time=time.time()


