import time
from threading import Thread

import cv2
import numpy as np

from Core.Basic import mkdir


def main():
	folder_L = mkdir(folder, "LCam")
	folder_R = mkdir(folder, "RCam")

	cap_L = cv2.VideoCapture(3)
	cap_R = cv2.VideoCapture(0)

	if cap_L.isOpened() and cap_R.isOpened():
		print(">> cameras start ..")
	else:
		print(">> err, can not open camera ..")
		exit(-1)

	value_L = np.empty(2, object)
	value_R = np.empty(2, object)
	display = np.zeros((144, 256), np.uint8)
	is_recording = False

	def func_L(i):
		ret, img = cap_L.read()
		if ret:
			img = img[::-1, ::-1]
			if is_recording:
				cv2.imwrite(folder_L + f"L{i:04d}.jpg", img)
		value_L[:] = ret, img

	def func_R(i):
		ret, img = cap_R.read()
		if ret:
			img = img[::-1, ::-1]
			if is_recording:
				cv2.imwrite(folder_R + f"R{i:04d}.jpg", img)
		value_R[:] = ret, img

	loop = 1
	count = 0
	t0 = time.time()
	while True:
		staff_L = Thread(target = func_L, args = (count,))
		staff_R = Thread(target = func_R, args = (count,))

		staff_L.start()
		staff_R.start()
		staff_L.join()
		staff_R.join()

		if value_L[0] and value_R[0]:
			img_L = value_L[1][::5, ::5]
			grayL = cv2.cvtColor(img_L, cv2.COLOR_BGR2GRAY)
			img_R = value_R[1][::5, ::5]
			grayR = cv2.cvtColor(img_R, cv2.COLOR_BGR2GRAY)

			display[:, :] = np.abs(grayL.astype(int) - grayR)
			cv2.imshow("cam", display)
		else: print(">> camera short circuit")

		key = cv2.waitKey(1)
		if key == 27: break
		if key == ord("s"):
			print(">> keyboard -> s")
			is_recording = not is_recording
		if is_recording: count += 1

		dt = time.time() - t0
		fps = loop / dt
		print(f"({count}, {dt:.3f}), fps = {fps:.1f}")
		loop += 1
	print(">> process finished ..")


if __name__ == '__main__':
	folder = "/Users/kaismac/Downloads/stereo_camera/"
	main()
	pass
