import os
import sys
import time
import subprocess
import string
import matplotlib.pyplot as plt


mydir=[]
tmplogfile = '/tmp/logcat.txt'
                
def get_logcat(filename):
	cmdline = "adb shell logcat -b events>%s" % (filename) 
	process = subprocess.Popen(cmdline,stdout=subprocess.PIPE,shell=True)
	print 'start get logcat.'
	for i in range(0,20):	
		time.sleep(0.10);
		print '.'
	process.terminate()

def process_logcat(filename):
        i=0
	file_object = open(filename,'r')
	for line in file_object:
		if line.startswith('I/boot'):
			mydir.append(line.split('): '))
			i+=1 
	return					
		
def plot_result(dir):
	i=0
	y=[]
	x=[]
	r=[]
	n=[]
	for value in dir:
		x.append(i)
		n.append(value[0][len('I/boot_progress_'):-1])
		y.append(string.atoi(value[1],10)/1000.0)
		i+=1
	for i in range(0,len(x)-1):
		r.append(y[i+1] - y[i])
	print y
	print x
	print r
	plt.title("Android Boot time events")
	plt.xlabel("events")
	plt.ylabel("Time(s)")
	plt.xticks(x,n)
	plt.xticks(rotation=90) 
	plt.plot(x,y)
	for i in range(0,len(x)):
		value="%.2f"%(y[i])
		plt.annotate(value,xy=(x[i], y[i]), xycoords='data',xytext=(x[i], y[i]), textcoords='offset points',fontsize=16,arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=.2"))
	plt.grid()
	plt.legend()
	plt.show()
	return
	
def reboot_android():
  	print 'reboot_android'
  	rv = os.system("adb reboot")
  	if rv != 0:
    		print "adb reboot failed"
    		sys.exit(1)
	return

def wait_android_boot_ok():
	print 'wait_android_boot_ok'
	while True:
		process = subprocess.Popen("adb shell getprop sys.boot_completed",stdout=subprocess.PIPE,stderr=None,shell=True)
		line = process.stdout.readlines();
		if len(line)>0:
			if line[0]=='1\r\n':
				break;
		time.sleep(0.1)
	return

def save_to_file(file_name):
	file_object = file(file_name,'w')
	#file_object.write(mydir.__str__())
	for value in mydir:
		file_object.write(value[0]);
		file_object.write('\r\n');
		file_object.write(value[1]);
	file_object.close()

def main(argv):
	
	reboot_android()
	wait_android_boot_ok()
	get_logcat(tmplogfile)
	process_logcat(tmplogfile)
	data_file_name = time.strftime("./%Y-%m-%d-%X.txt", time.localtime())
	save_to_file(data_file_name)
	plot_result(mydir)

	
if __name__=="__main__":
        main(sys.argv)
