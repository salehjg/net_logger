import socket
import datetime
import numpy as np
import time

REMOTE_SERVER = "www.google.com"
ON_BOOT_DELAY_S = 60

def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False

def log_onestep():
	x = datetime.datetime.now()
	datetime_str = (x.strftime("%c")) 
	connection_status = is_connected(REMOTE_SERVER)
	return np.array([datetime_str, connection_status])

def start_logging(delay_s, freq_print, freq_dump):
	array = np.empty([0,3])
	print array.shape
	cnt = 0
	while True:
		time.sleep(delay_s)
		cnt=cnt+1
		retval = log_onestep()
		retval = np.insert(retval,0,cnt,axis=0)
		retval = np.reshape(retval, newshape=[1,3])
		array=np.append(array,retval,axis=0)
		if freq_print>=0:
			if cnt%freq_print is 0:
				print array
		if cnt%freq_dump is 0:
			print 'dumping logs and flushing buffer'
			fname = time.strftime("%Y%m%d-%H%M%S")
			np.save('/home/pi/00_workspaces/4_python/ping_logger/logs/' + fname + '.npy', array)
			array = np.empty([0,3])

print 'initial delay on boot(' + str(ON_BOOT_DELAY_S) + ' seconds)'
time.sleep(ON_BOOT_DELAY_S)
start_logging(delay_s=1, freq_print=-1, freq_dump=900)


