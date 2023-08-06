from threading import Thread

class WorkerThread(Thread):
	def __init__(self, func, *args):
		Thread.__init__(self, name='polling...')
		self.func = func
		self.args = args
		self._running = True
		self.start()
		
	def run(self):
		try:
			return self.func(*self.args)
		except Exception as e:
			print(f"Ошибка из файла WorkerThread: " + str(e))
			

