import matplotlib.pyplot as p

def plotTest():
	print "PLOTTED!"

def plotEnergyVsTime(energy,name):
	p.clf()
	ax=p.axes()
	timesteps=range(1,len(energy)+1)
	ax.plot(timesteps,energy)
	p.xlabel('Time Step')
	p.ylabel('Energy Level')
	p.title('Energy Over Time')
	p.savefig(name)

def plotVelocityVsSurvival(velocities, survivalDurations, name):
	p.clf()
	ax=p.axes()
	ax.bar(velocities,survivalDurations,linewidth=1,c='blue',label='trainingRMS')
	p.xlabel("Velocity ")
	p.ylabel("Survival Duration")
	p.title("Velocity Vs. Survival Duration")
	p.savefig(name)

def plotWeightChangeVsEpoch(weightChange, epochNumber, name):    
    p.clf()
    ax=p.axes()
    epochs=range(1,epochNumber)
    ax.plot(epochs,weightChange,linewidth=1,c='blue',label='trainingRMS')
    p.xlabel("Epoch Number")
    p.ylabel("Weight Change")
    p.title("Weight Change vs Epoch")
    p.xlim([0,epochNumber+1])
    p.savefig(name+'.png')

def plotEyeColorWeights():
	p.clf()
	ax=p.axes()
	bias,R,G,B,presentation=[],[],[],[],[]
	f=open('./eyecolor.txt','r').read().replace(' ','').split('\n')[0:-1]
	presentationNumber=1
	for data in f:
		data=data[1:-1].split(',')
		bias.append(float(data[0]))
		R.append(float(data[1]))
		G.append(float(data[2]))
		B.append(float(data[3]))
		presentation.append(presentationNumber)
		presentationNumber+=1
	p.xlabel('Presentation Number')
	p.ylabel('Weight Value')
	p.title('Weight Change over Presentation')
	ax.plot(presentation,bias,c='black',label='bias')
	ax.plot(presentation,R,c='red',label='red')
	ax.plot(presentation,G,c='green',label='green')
	ax.plot(presentation,B,c='blue',label='blue')
	p.legend(loc='lower left')
	p.savefig('weightChangeVsPres-new-bluelearn.png')

plotEyeColorWeights()
















