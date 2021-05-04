import threading
import time

import cv2
import numpy as np


def main():
	cap_L = cv2.VideoCapture(3)
	cap_R = cv2.VideoCapture(0)
	# cap_L.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	# cap_R.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	# cap_L.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	# cap_R.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	if cap_L.isOpened() and cap_R.isOpened():
		print(">> cameras start ..")
	else:
		print(">> err, can not open camera ..")
		exit(-1)

	display_W = 400
	display_H = 225
	display = np.zeros((display_H * 3, display_W * 3, 3), np.uint8)

	def multi_display(images):
		for i, src in enumerate(images):
			if src is None: continue
			dst = cv2.resize(src, (display_W, display_H))
			if len(dst.shape) < 3:
				dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
			y, x = i // 3 * display_H, i % 3 * display_W
			display[y:y + display_H, x:x + display_W, :] = dst[::-1, ::-1]
		return display

	value_L = np.empty(2, object)
	value_R = np.empty(2, object)
	is_running = True
	imgs = np.empty(9, object)
	thread_lock = threading.Lock()

	class StaffL(threading.Thread):
		def run(self):
			value_L[:] = ret, img = cap_L.read()
			if ret:
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (11, 11), 10)
				thread_lock.acquire()
				imgs[0] = img
				imgs[1] = gray
				thread_lock.release()
		pass

	class StaffR(threading.Thread):
		def run(self):
			value_R[:] = ret, img = cap_R.read()
			if ret:
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (11, 11), 10)
				thread_lock.acquire()
				imgs[3] = img
				imgs[4] = gray
				thread_lock.release()
		pass

	t0 = time.time()
	count = 1
	while is_running:
		imgs = np.empty(9, object)

		staff_L = StaffL()
		staff_R = StaffR()
		staff_L.start()
		staff_R.start()
		staff_L.join()
		staff_R.join()

		if value_L[0] and value_R[0]:
			imgs[6] = (imgs[0] / 2 + imgs[3] / 2).astype(np.uint8)
			imgs[7] = (imgs[1] / 2 + imgs[4] / 2).astype(np.uint8)
			imgs[8] = np.abs(np.asarray(imgs[1], int) - imgs[4]).astype(np.uint8)

			cv2.imshow("cam", multi_display(imgs))
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
