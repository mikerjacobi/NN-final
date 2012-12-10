import matplotlib.pyplot as p
import math

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

def barTwoVar(v1,v2,v1lab,v2lab,name):
    p.clf()
    p.xlabel(v1lab)
    p.ylabel(v2lab)
    p.title(name)
    p.bar(v1,v2)
    p.savefig(name+'.png')


def plotTwoVar(x,y,labels,xlab,ylab,colors,name,location):
	p.clf()
	#ax=p.axes()
	for i in range(len(x)):
		if colors==None:
			p.plot(x[i],y[i],label=labels[i])
		else: 
			p.plot(x[i],y[i],label=labels[i],color=colors[i])


	p.xlabel(xlab)
	p.ylabel(ylab)
	p.title(name.split('/')[-1])
	p.legend(loc=location)
	p.savefig(name+'.png')

def brain1Velocity():
    f=open('brain1/velocity2.txt','r').read().split('\n')[0:-1]
    samples,data=[],[]
    for l in f:
        record=l.split(',')
        samples.append(float(record[4]))
        data.append(float(record[2]))
        
    plotTwoVar(samples,data,'velocity','timesteps survived','brain1/velocity_vs_survival')

def standardDeviation(x):
	mean=0
	numVals=len(x)
	for i in range(numVals):
		mean+=x[i]
	mean=float(mean)/numVals
	stddev=0
	for i in range(numVals):
		stddev+=(mean-x[i])**2
	stddev=round(math.sqrt(float(stddev)/numVals),2)
	return stddev

def plotSurvivalGaussian(brain,bucketSize):
	f=open(brain+'/'+brain+'data.txt','r').read().split('\n')[0:-1]
	data={}
   	
	for l in f:
		record=l.split(',')
		currVal=int(record[2])/bucketSize*bucketSize
		try: data[currVal]+=1
		except: data[currVal]=1

	x,y,labels,currX,currY=[],[],[],[],[]
	for k in sorted(data.keys()):
		currX.append(k)
		currY.append(data[k])
	x.append(currX)
	y.append(currY)
	stddev=standardDeviation(currX)

	#plotTwoVar(x,y,labels,'Survival Duration Bucket','Epoch Count',None,brain+'/survivalGauss-'+str(stddev), 'upper left')

	
	p.clf()
	for i in range(len(x)):
		p.plot(x[i],y[i])

	p.xlabel('Survival Duration Bucket')
	p.ylabel('Epoch Count')
	p.title('Survival Duration Distribution')
	#p.legend(loc='upper left')
	p.savefig(brain+'/survivalGauss-'+str(stddev)+'.png')

def plotAvgEnergyGaussian(brain,roundoff):
	f=open(brain+'/'+brain+'data.txt','r').read().split('\n')[0:-1]
	data={}
	testdata=[]
	for l in f:
		record=l.split(',')
		#currVal=float('%.3f'%float(record[3]))
		currVal=int(float(record[3])*100)
		testdata.append(currVal)
        try: data[currVal]+=1
        except: data[currVal]=1
	data={}
	for test in testdata:
		try: data[float(test)/100]+=1
		except: data[float(test)/100]=1
	currX,currY=[],[]
	for k in sorted(data.keys()):
		currX.append(k)
		currY.append(data[k])
	stddev=standardDeviation(currX)

	p.clf()
	#ax=p.axes()
	p.plot(currX,currY)
   	p.xlim((0,1)) 
	p.ylabel('Epoch Count')
	p.xlabel('Average Energy throughout Epoch Life')
	p.title('Average Energy per Epoch Distrubtion')
	#p.legend(loc='upper left')
	p.savefig(brain+'/avgenergyGauss-'+str(stddev)+'.png')


def plotHPNgauss(brain):
	f=open(brain+'/'+brain+'data.txt','r').read().split('\n')[0:-1]
	health,poison,neutral={},{},{}
	for l in f:
		record=l.split(',')
		try:health[int(record[5])]+=1
		except:health[int(record[5])]=1
		try:poison[int(record[7])]+=1
		except:poison[int(record[7])]=1
		try:neutral[int(record[6])]+=1
		except:neutral[int(record[6])]=1

	healthX,healthY=[],[]
	for k in sorted(health.keys()):
		healthX.append(k)
		healthY.append(health[k])
	neutralX,neutralY=[],[]
	for k in sorted(neutral.keys()):
		neutralX.append(k)
		neutralY.append(neutral[k])
	poisonX,poisonY=[],[]
	for k in sorted(poison.keys()):
		poisonX.append(k)
		poisonY.append(poison[k])
	x=[healthX,neutralX,poisonX]
	y=[healthY,neutralY,poisonY]
	healthSD=str(standardDeviation(healthX))
	neutralSD=str(standardDeviation(neutralX))
	poisonSD=str(standardDeviation(poisonX))
	sdString="h%s-n%s-p%s"%(healthSD,neutralSD,poisonSD)
	#s='sigma='
	#labels=[s+healthSD,s+neutralSD,s+poisonSD]
	labels=['health','neutral','poison']
	colors=['green','blue','red']
	
	#plot	
	p.clf()
	for i in range(len(x)):
		p.plot(x[i],y[i],label=labels[i],color=colors[i])
	p.xlabel('Food Items Eaten')
	p.ylabel('Epoch Count')
	p.title('Food Eaten Distribution')
	p.legend(loc='upper right')
	p.savefig(brain+'/foodGauss-'+sdString+'.png')

def barVar(variable,ylabel,name,filename,c):
	#open up each data file
	means=[]
	stddevs=[]
	brains=[]
	for i in range(8): brains.append('brain'+str(i))
	for brain in brains:
		f=open(brain+'/'+brain+'data.txt','r').read().split('\n')[:-1]
		currMean=0
		currData=[]
		for i in range(len(f)): 
			currValue=float(f[i].split(',')[variable])
			currData.append(currValue)
			currMean+=currValue
		stddevs.append(standardDeviation(currData))
		currMean/=len(f)
		means.append(currMean)
			
	#plot 
	p.clf()
	p.xlabel('Brain Number')
	p.ylabel(ylabel)
	p.title(name)
	p.bar(range(8),means,color=c,yerr=stddevs)

	sdString='-'
	for sd in stddevs:
		sdString+=str(sd)+'-'

	p.savefig(filename+sdString[0:-1]+'.png')

def plotDRgauss(brain):
	f=open(brain+'/'+brain+'data.txt','r').read().split('\n')[0:-1]
	distance,rotation={},{}
	for l in f:
		record=l.split(',')
		r=int(record[8])/300*300
		d=int(record[9])/400*400
		try:rotation[r]+=1
		except:rotation[r]=1
		try:distance[d]+=1
		except:distance[d]=1	
	rotationX,rotationY=[],[]
	for k in sorted(rotation.keys()):
		rotationX.append(k)
		rotationY.append(rotation[k])
	distanceX,distanceY=[],[]
	for k in sorted(distance.keys()):
		distanceX.append(k)
		distanceY.append(distance[k])
	x=[rotationX,distanceX]
	y=[rotationY,distanceY]
	rotationSD='%.2f'%standardDeviation(rotationX)
	distanceSD='%.2f'%(standardDeviation(distanceX))
	sdString="r%s-d%s"%(rotationSD,distanceSD)
	#s='sigma='
	labels=['degrees rotated','distance traveled forward']
	colors=['red','blue']
	#labels=['units: degrees rotated\n'+s+rotationSD,'units: distance traveled\n'+s+distanceSD]

	#make the plot
	
	p.clf()
	for i in range(len(x)):
		p.plot(x[i],y[i],label=labels[i],color=colors[i])

	p.xlabel('Degrees Rotated/Forward Motion')
	p.ylabel('Epoch Count')
	p.title('Movement Distribution')
	p.legend()
	p.savefig(brain+'/travelGauss-'+sdString+'.png')












