import pykka
import time
from apscheduler.schedulers.background import BackgroundScheduler

class Printer:
	'''Printer'''

	def __init__(self):
		self.mesg='toot'

	def set_mesg(self, mesg):
		self.mesg=mesg

	def display(self):
		print(self.mesg)


class Greeter(pykka.ThreadingActor):
	'''Greeter'''

	def __init__(self, greeting='Hi there!'):
		super(Greeter, self).__init__()
		self.printer = Printer()
		self.greeting = greeting
		self.sched = BackgroundScheduler()
		self.job = self.sched.add_job(self.printer.display, 'interval', minutes=0.01)
		self.sched.start()

	def on_receive(self, message):
		if (message['msg']=='Stop!'):
			self.sched.shutdown()
			self.stop()
		else:
			self.printer.set_mesg(message['msg'])

actor_ref = Greeter.start(greeting='Hi you!')
time.sleep(2)
actor_ref.tell({'msg': 'Hi?'})
time.sleep(2)
actor_ref.tell({'msg': 'Ho?'})
time.sleep(2)
actor_ref.tell({'msg': 'Stop!'})
