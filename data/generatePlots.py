import plotting as p

def generatePlots():
	#(0 self.startTime,
	#1 survivalTime,self.
	#2 numTimesteps,
	#3 averageEnergy,self.
	#4 constantFB,self.
	#5 healthEaten,self.
	#6 neutralEaten,self.
	#7 poisonEaten,self.
	#8 totalRotation,self.
	#9 distanceTraveled,
	#10 numConnections,
	#11 numNeurons,
	#12 numNetworks)

	#calculate plots per brain
	brains=[]

	#survival bucketsizes
	sbs={0:10,1:10,2:50,3:250,4:500,5:1000,6:1000,7:1000}	

	for i in range(8): brains.append('brain'+str(i))
	for brain in brains:
		print 'producing plots for',brain
		#create a gaussian of timestep
		p.plotSurvivalGaussian(brain,sbs[int(brain[-1])])
		
		#average energy gaussian
		p.plotAvgEnergyGaussian(brain,2)

		#health,poison,neutral combo gauss
		p.plotHPNgauss(brain)
		
		#distance,rotation combo gauss
		p.plotDRgauss(brain)

	#cross brain plots
	print 'generating cross-brain plots'

	#p.barVar(variable number, ylabel, plot title, save filename)
	#avgtimestepsa
	p.barVar(2,'Average Timesteps Survived','Survival Duration per Epoch as Brain Sophistication Increases', 'survivalBar','orange')	

	#avgavgenergy
	p.barVar(3,'Average Energy', 'Average Energy per Epoch as Brain Sophistication Increases', 'avgEnergyBar','orange')
	
	#avgHPN
	p.barVar(5,'Green Food Eaten', 'Green Food Eaten per Epoch as Brain Sophistication Increases', 'greenBar','green')
	p.barVar(6,'Blue Food Eaten', 'Blue Food Eaten per Epoch as Brain Sophistication Increases', 'blueBar','blue')
	p.barVar(7,'Red Food Eaten', 'Red Food Eaten per Epoch as Brain Sophistication Increases', 'redBar','red')

	#avgDistancetraveled
	p.barVar(9,'Distance Traveled', 'Distance Traveled per Epoch as Brain Sophistication Increases', 'distanceBar','orange')

	#connections/neurons/networks
	p.barVar(10,'Number of Neural Connection', 'Neural Connection Number as Brain Sophistication Increases', 'connectionBar','orange')
	p.barVar(11, 'Number of Neurons', 'Neuron Count as Brain Sophistication Increases', 'neuronBar','orange')
	p.barVar(12, 'Number of Neural Networks', 'Neural Network Count as Brain Sophistication Increases', 'networkBar','orange')
	








generatePlots()
