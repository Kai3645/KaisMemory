import threading
import time

import cv2
import numpy as np


def main():
	cap_L = cv2.VideoCapture(3)
	cap_R = cv2.VideoCapture(0)

	if cap_L.isOpened() and cap_R.isOpened():
		print(">> cameras start ..")
	else:
		print(">> err, can not open camera ..")
		exit(-1)

	value_L = np.empty(2, object)
	value_R = np.empty(2, object)
	display = np.zeros((720 * 2, 1280, 3), np.uint8)
	is_running = True

	class StaffL(threading.Thread):
		def run(self):
			value_L[:] = cap_L.read()
			value_L[1] = value_L[1][::-1, ::-1]

		pass

	class StaffR(threading.Thread):
		def run(self):
			value_R[:] = cap_R.read()
			value_R[1] = value_R[1][::-1, ::-1]

		pass

	count = 1
	t0 = time.time()
	while is_running:
		staff_L = StaffL()
		staff_R = StaffR()
		staff_L.start()
		staff_R.start()
		staff_L.join()
		staff_R.join()

		if value_L[0] and value_R[0]:
			display[:720, :, :] = value_L[1]
			display[720:, :, :] = value_R[1]
			cv2.imshow("cam", display)
			if cv2.waitKey(1) == 27:
				is_running = False
				print(">> exit ..")
		else: print(">> camera short circuit")

		dt = time.time() - t0
		fps = count / dt
		print(f"({count}, {dt:.3f}), fps = {fps:.1f}")
		count += 1
	print(">> process finished ..")


if __name__ == '__main__':
	main()
	pass
