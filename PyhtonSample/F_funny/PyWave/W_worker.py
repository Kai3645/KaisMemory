import threading
import time

import numpy as np

from A_core.B_KaisLog import KaisLog


class Staff(threading.Thread):
	def __init__(self, ID, neighbor):
		threading.Thread.__init__(self, name = "Staff_%02d " % ID)
		self.ID = ID
		self.img = None
		self.wxImg = None
		self.bitmap = None
		self.neighbor = neighbor

	def run(self):
		myLog.push("start working .. ")

		while 1:
			# myLog.push("holding .. ")
			if self.img is None: continue
			myLog.lock_ac()
			self.img += 1
			time.sleep(2)
			self.neighbor.img = self.img
			self.wxImg = self.img + 100
			self.bitmap = self.wxImg + 10000
			myLog.lock_re()
			self.img = None
			time.sleep(2)
			myLog.push("result: %d", self.bitmap)

		myLog.push("work finished .. ")


def main_process(worker: Staff):
	start_num = 0
	for _ in range(1000):
		worker.img = start_num
		myLog.push("show: " + str(worker.bitmap))
		time.sleep(10)
	pass


def main():
	myLog.push("work start .. ")

	staffs = np.empty(5, Staff)
	next_worker = None
	for i in range(5):
		staffs[i] = Staff(i, next_worker)
		next_worker = staffs[i]
	staffs[0].next = next_worker

	for s in staffs: s.start()

	leader = threading.Thread(
			name = "leader",
			target = main_process,
			args = (staffs[0],),
	)
	leader.start()

	leader.join()
	for s in staffs: s.join()

	myLog.push("all jobs finished .. ")


if __name__ == '__main__':
	threading.current_thread().setName("main")

	f_main = "/Users/kaismbp/virtualenvs/myProject/output"
	myLog = KaisLog(folder = f_main, lock = threading.Lock())

	myLog.push("process start .. ")

	main()

	myLog.push("process finished .. ")
