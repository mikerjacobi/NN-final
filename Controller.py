#!/usr/bin/python
# Nasser Salim & Renzo Sanchez-Silva
# CS547 - Neural Networks

import sys
import random
import logging


# I don't know why but Python.h needs this to see local modules
sys.path.append('.')
sys.path.append('./brains')
#from Stats import Stats
#from Logger import Log

from BrainX import BrainX
from Brain0 import Brain0
from Brain1 import Brain1
from Brain2 import Brain2
from Brain3 import Brain3
from Brain4 import Brain4
from Brain5 import Brain5
from Brain6 import Brain6

class Controller:
	def __init__(self):
		self.brain = BrainX()
		self.installed_brains = {
			-1:BrainX,
			0:Brain0,
			1:Brain1,
			2:Brain2,
			3:Brain3,
			4:Brain4,
			5:Brain5,
			6:Brain6,
		}
	
	def set_brain(self, brain):
		brain=6
		self.brain_id = brain
		if brain not in self.installed_brains:
			raise ValueError, "Unknown brain %d" % brain
		print "Using brain", brain
		self.brain = self.installed_brains[brain]()
    
	def verbose(self):
		pass
        #self.log.setLevel(logging.DEBUG)
        #self.stats.log.setLevel(logging.DEBUG)


	def reset(self):
		pass
		#self.stats.reset()
	
	def run_brain(self, args):
		[charge, touch, eye, ear0, ear1, actuators, headangle] = args
		#sys.stderr.write("Iteration %d - %.2f%%   \r" % (self.stats.iteration, charge*100) )
		#sys.stderr.write("test")
		return self.brain.run(charge, touch, eye, ear0, ear1, actuators, headangle)

    
	def learn(self, dcharge):
		self.brain.learn(dcharge)

	def process_stats(self,data):
		self.brain.process_stats(data)
		'''
		global survivalDuration,numFoodEaten,distanceFromOrigin
		survivalDuration+=1
		if data[-2]==1: numFoodEaten+=1
		distanceFromOrigin+=data[2][0]
		'''
	
	def reset(self):
		self.brain.reset()
		'''
		global survivalDuration,numFoodEaten,distanceFromOrigin
		f=open('test.txt','w')
		f.write('survival duration: %d\n'%survivalDuration)
		f.write('number foods eaten: %d\n'%numFoodEaten)
		f.write('distance from center: %f\n'%distanceFromOrigin)
		f.close()
		survivalDuration=0
		numFoodEaten=0
		distanceFromOrigin=0
		'''

controller = Controller()

