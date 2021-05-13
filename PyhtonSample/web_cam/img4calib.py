import time

import cv2

from Core.Basic import mkdir, err_exit
from Core.ComputerVision.camera_basic import chessboard_corner_detect, chessboard_draw_corner, chessboard_area_ratio
from Core.ComputerVision.image_basic import gray2binary

if __name__ == '__main__':
	folder = mkdir("/Users/kaismac/Downloads", "C922_calib")

	BOARD_W = 8
	BOARD_H = 5
	BOARD_SHAPE = (BOARD_W, BOARD_H)
	IMAGE_W = 1280
	IMAGE_H = 720
	IMAGE_SHAPE = (IMAGE_W, IMAGE_H)
	AREA_RATIO_MAX = 0.40
	AREA_RATIO_MIN = 0.25

	cap = cv2.VideoCapture(2)
	if cap.isOpened(): print(">> cameras start ..")
	else: err_exit(">> err, can not open camera ..")


	def process(image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		binary = gray2binary(gray)
		corners = chessboard_corner_detect(gray, BOARD_SHAPE, binary)
		if corners is None: return False, binary

		area_ratio = chessboard_area_ratio(corners, BOARD_SHAPE, IMAGE_SHAPE)
		if area_ratio < AREA_RATIO_MIN or area_ratio > AREA_RATIO_MAX:
			return False, chessboard_draw_corner(img, corners, cname = "cool")
		return True, chessboard_draw_corner(img, corners, cname = "hsv")


	loop = 0
	shooting = False
	t0 = time.time()
	while True:
		ret, img = cap.read()
		if ret:
			ret, dst = process(img)
			cv2.imshow("cam", dst[::3, ::3])
			if ret and shooting:
				cv2.imwrite(folder + f"{loop:05d}.jpg", img)
		else: print(">> camera short circuit")
		key = cv2.waitKey(1)
		if key == 27: break
		if key == ord("s"):
			shooting = not shooting
			print("start shooting")

		loop += 1
		dt = time.time() - t0
		fps = loop / dt
		print(f"{loop}, {fps:.1f}")
	print(">> process finished ..")
	pass
