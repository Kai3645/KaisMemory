import time
from threading import Thread

import cv2
import numpy as np

from Core.Basic import mkdir
from Core.ComputerVision.camera_basic import chessboard_corner_detect, chessboard_draw_corner, chessboard_area_ratio
from Core.ComputerVision.image_basic import gray2binary


def main():
	folder_L = mkdir(folder, "LCam")
	folder_R = mkdir(folder, "RCam")

	board_shape = (8, 5)
	image_shape = (1280, 720)

	cap_L = cv2.VideoCapture(0)
	cap_R = cv2.VideoCapture(3)

	if cap_L.isOpened() and cap_R.isOpened():
		print(">> cameras start ..")
	else:
		print(">> err, can not open camera ..")
		exit(-1)

	value_L = np.empty(3, object)
	value_R = np.empty(3, object)
	display = np.zeros((720, 640, 3), np.uint8)

	def process(img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		binary = gray2binary(gray)
		corners = chessboard_corner_detect(gray, board_shape, binary)
		if corners is None: return False, img

		area_ratio = chessboard_area_ratio(corners, board_shape, image_shape)
		if area_ratio < 0.15 or area_ratio > 0.40:
			return False, chessboard_draw_corner(img, corners, cname = "cool")
		return True, chessboard_draw_corner(img, corners, cname = "hsv")

	def func_L():
		dst = None
		ret, img = cap_L.read()
		if ret:
			img = img[::-1, ::-1]
			ret, dst = process(img)
		value_L[:] = ret, dst, img

	def func_R():
		dst = None
		ret, img = cap_R.read()
		if ret:
			img = img[::-1, ::-1]
			ret, dst = process(img)
		value_R[:] = ret, dst, img

	loop, count = 0, 0
	t0 = time.time()
	while True:
		display[:, :, :] = 0
		staff_L = Thread(target = func_L)
		staff_R = Thread(target = func_R)

		staff_L.start()
		staff_R.start()
		staff_L.join()
		staff_R.join()

		if value_L[0] and value_R[0]:
			print(count)
			cv2.imwrite(folder_L + f"L{count:06d}.jpg", value_L[2])
			cv2.imwrite(folder_R + f"R{count:06d}.jpg", value_R[2])
			count += 1
		if value_L[1] is not None:
			display[:360, :, :] = value_L[1][::2, ::2, :]
		if value_R[1] is not None:
			display[360:, :, :] = value_R[1][::2, ::2, :]
		cv2.imshow("cam", display)

		key = cv2.waitKey(1)
		if key == 27: break

		loop += 1
		dt = time.time() - t0
		fps = loop / dt
		print(f"{loop}, {fps:.1f}, {value_L[0]}, {value_R[0]}, {count}")
	print(">> process finished ..")


if __name__ == '__main__':
	folder = "/Users/kaismac/Downloads/stereo_camera/"
	main()
	pass
