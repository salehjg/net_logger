import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

def plot(xdata):
	time = np.arange(0,xdata.shape[0])
	f = plt.figure()
	ax = f.add_subplot(111)
	p = ax.plot(time, xdata, "r--", label="Status")
	ax.grid(True)
	ax.set_xlabel("Time Indices")
	ax.set_ylabel("0:Disconnected, 1:Connected")
	ax.set_title("Connection Status")
	ax.axis("tight")
	plt.legend(loc='best')
	axes = plt.gca()
	axes.set_ylim([-1,2])
	plt.show()

def dump_period(startDC, stopDC):
	print '------------------------------------------'
	print 'Network Intruption Period:'
	print '** start:   ' + str(startDC)
	print '** stop:    ' + str(stopDC)

def main_analysis(fname, array=[]):
	if(fname==""):
		logs = array
	else:
		logs = np.load(fname)
	idlen = logs.shape[0]
	#print 'logfile shape = ' + str(logs.shape)
	dc = False
	for i in range(0,idlen):
		#print logs[i,2]
		if dc == False:
			if logs[i,2] == 'False':
				dc=True
				startDC = logs[i,]
		else:
			if logs[i,2] == 'True':
				dc=False
				stopDC = logs[i,]
				dump_period(startDC,stopDC)
	stats = convert_data(logs)
	plot(stats)

def convert_data(array):
	values = np.zeros([array.shape[0]], dtype=np.int32)
	for i in range(0,array.shape[0]):
		values[i] = 1 if array[i,2]=='True' else 0
	return values

if __name__ == '__main__':
   # main_plot()
	print 'Arg Count:'+str(len(sys.argv))
	if len(sys.argv)==2:
		print 'Loading the specified file in the argument'
		main_analysis(sys.argv[1])
	else:
		mypath = './logs/'
		print 'Concatenating all of the logs in logs directory...'
		onlyfiles = ['logs/'+f for f in listdir(mypath) if isfile(join(mypath, f))]
		print 'Found '+ str(len(onlyfiles)) + ' files. Concatenating...'
		idx = 0
		for f in onlyfiles:
			ff = np.load(f)
			concat = ff if idx==0 else np.concatenate((concat,ff),axis=0)
			idx=idx+1
		print 'Concatenation done. Final log shape: ' + str(concat.shape)
		main_analysis("",concat)
		
