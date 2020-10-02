import threading
import time


class Staff(threading.Thread):
	def __init__(self, ID):
		threading.Thread.__init__(self, name = "Staff_%02d " % ID)
		self.ID = ID

	def run(self):
		myLog.push("start working .. ")

		while 1:
			exit_flag, new_job = job_manager()
			if exit_flag: break
			myLog.push("got job[%d] " % new_job)
			time.sleep(1)

		myLog.push("work finished .. ")


def job_manager():
	myLog.lock_ac()
	if not jobs:
		myLog.lock_re()
		return True, None
	temp_job = jobs[-1]
	jobs.pop()
	myLog.lock_re()
	return False, temp_job


def main():
	myLog.push("work start .. ")

	staffs = []
	for i in range(10): staffs.append(Staff(i))
	for s in staffs: s.start()
	for s in staffs: s.join()

	myLog.push("all jobs finished .. ")


def create_jobs():
	temp_jobs = [i for i in range(32)]
	return temp_jobs


if __name__ == '__main__':
	threading.current_thread().setName("Main")
	folder = "/Users/kai/ProjectCenter/MELCO_Project/temp_out/"
	myLog = KaisLog(folder = folder, lock = threading.Lock())

	myLog.push("process start .. ")

	jobs = create_jobs()

	main()

	myLog.push("process finished .. ")
