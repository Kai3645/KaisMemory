import threading
import queue
import time


def push_info(info, lock):
	lock.acquire()
	tmp_str = time.strftime("%H:%M:%S ", time.localtime())
	tmp_str += threading.current_thread().getName() + " >> " + info
	print(tmp_str)
	lock.release()


def job_manager(jobs, lock):
	job = None
	num = jobs.qsize()
	if num == 0:
		push_info("no more jobs ..", lock)
		return False, job
	job = jobs.get(block = True)
	jobs.task_done()
	return True, job


def create_jobs():
	jobs = queue.Queue(6)
	for i in range(6):
		jobs.put(i, block = True)
	return jobs


class Staff(threading.Thread):
	def __init__(self, ID, jobs, lock):
		threading.Thread.__init__(self, name = "Staff_%02d " % ID)
		self.ID = ID
		self.lock = lock
		self.jobs = jobs

	def run(self):
		push_info("start working .. ", self.lock)
		while True:
			got_job, new_job = job_manager(self.jobs, self.lock)
			if not got_job: break
			push_info("got job[%d] " % new_job, self.lock)
		# time.sleep(1)
		push_info("work finished .. ", self.lock)


if __name__ == "__main__":
	temp_jobs = create_jobs()
	thread_lock = threading.Lock()
	staffs = [
		Staff(0, temp_jobs, thread_lock),
		Staff(1, temp_jobs, thread_lock),
		Staff(2, temp_jobs, thread_lock),
	]
	for s in staffs: s.start()
	for s in staffs: s.join()

	temp_jobs.join()
