from datetime import datetime, timedelta
import util, time, signal, threading
import conf

database = {}

current_prediction_time = None
current_prediction_value = None

next_predition_time = None
next_predition_value = None

callback = None

timer = None

exit = False

def set_callback(cb):
	global callback
	callback = cb

def stop():
	global timer, exit
	if timer:
		timer.cancel()
	exit = True

def process():
	global callback, database, timer

	# now
	now = datetime.now()
	(c, n) = util.next(now, database)

	current_prediction_time = c
	current_prediction_value = database[c]
	next_predition_time = n
	next_predition_value = database[n]

	if callback:
		callback((current_prediction_value, current_prediction_time, next_predition_value, next_predition_time))

	sleep_dt = next_predition_time - now

	# print "&&&&&&&&&&&&&&&&&&&&&&&&"
	# print current_prediction_time
	# print current_prediction_value
	# print "-----"
	# print now
	# print next_predition_time
	# print "sleep for: "
	# print next_predition_time - now

	# time.sleep(sleep_dt.total_seconds())

	timer = threading.Timer(sleep_dt.total_seconds(), process)
	timer.start()


def run(block=True):
	# ex. 09/06/2017  01:00
	datetime_format = '%d/%m/%Y  %H:%M'

	with open(conf.filename_tide_predictions) as f:
		first = True
		for line in f:
			if(first):
				first = False
				continue
			l = line.strip().split('    ')
			d = datetime.strptime(l[0], datetime_format)
			# set to British Summer Time (BST) (re: +1 hour)
			d = d + timedelta(hours=1);
			v = float(l[1])

			database[d] = v

	process()

	if block:
		while not exit:
			try:
				time.sleep(2)
			except KeyboardInterrupt as e:
				print "got exception"
				stop()
				break
		


if(__name__ == '__main__'):

	signal.signal(signal.SIGTERM, stop)
	signal.signal(signal.SIGQUIT, stop)
	signal.signal(signal.SIGHUP, stop)

	run()

