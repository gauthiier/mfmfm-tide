import time, threading, signal, sys, OSC
from datetime import datetime
import tide_prediction, tide_prediction_hlw
import conf

client = OSC.OSCClient()

def thread_prediction_cb(v):
	global client
	print "thread_prediction_cb"

	oscmsg = OSC.OSCMessage()
	oscmsg.setAddress(conf.MOUNT_POINT)
	oscmsg.append(v[0])									# current_prediction_value
	oscmsg.append(v[1].strftime("%Y-%m-%d %H:%M"))		# current_prediction_time
	oscmsg.append(v[2])									# next_predition_value
	oscmsg.append(v[3].strftime("%Y-%m-%d %H:%M"))		# next_predition_time

	try:
		client.send(oscmsg)	
	except:
		print "no connection... continuing"

def thread_prediction_hlw_cb(v):
	global client
	print "thread_prediction_hlw_cb"

	oscmsg = OSC.OSCMessage()
	oscmsg.setAddress(conf.MOUNT_POINT_HLW)
	oscmsg.append(v[0])										# current_prediction_value
	oscmsg.append(v[1].strftime("%Y-%m-%d %H:%M"))			# current_prediction_time
	oscmsg.append(v[2])										# current_prediction_type ('H', 'L')
	oscmsg.append(v[3])										# next_prediction_value
	oscmsg.append(v[4].strftime("%Y-%m-%d %H:%M"))			# next_prediction_time
	oscmsg.append(v[5])										# next_prediction_type ('H', 'L')

	try:
		client.send(oscmsg)	
	except:
		print "no connection... continuing"


if(__name__ == '__main__'):

	client.connect((conf.HOST, conf.PORT))

	tide_prediction.set_callback(thread_prediction_cb)
	tide_prediction_hlw.set_callback(thread_prediction_hlw_cb)

	tide_prediction.run(block=False)
	tide_prediction_hlw.run(block=False)

	while True:
		try:
			time.sleep(2)
		except KeyboardInterrupt as e:
			print "exiting..."
			tide_prediction.stop()
			tide_prediction_hlw.stop()
			sys.exit(1)




