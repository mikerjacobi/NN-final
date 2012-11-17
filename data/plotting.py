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
