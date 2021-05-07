import time
from threading import Thread

import cv2
import numpy as np

from Core.Basic import mkdir
from Core.Visualization import KaisCanvas


def main():
	mat_L = np.asarray([371.7238, 0.0000, 603.0837, 0.0000, 371.6990, 349.0501, 0.0000, 0.0000, 1.0000]).reshape([3, 3])
	mat_R = np.asarray([372.4407, 0.0000, 626.7559, 0.0000, 372.5443, 362.9187, 0.0000, 0.0000, 1.0000]).reshape([3, 3])
	dist_L = np.asarray([2.58339740, 4.27790321, -0.00000468, 0.00133856, 0.04181726, 2.31375616, 3.64480336,
	                     0.37388115, -0.00173613, 0.00014957, -0.00010390, -0.00005456, 0.00259686, 0.00150627])
	dist_R = np.asarray([2.85419397, 4.41270687, 0.00016594, 0.00290789, 0.07042960, 2.57469084, 3.74501496,
	                     0.42086447, -0.00147710, -0.00023769, -0.00066186, 0.00004257, 0.00026240, 0.01072015])
	R = np.asarray([0.99990214, 0.00522852, 0.01297612,
	                -0.00524353, 0.99998562, 0.00112295,
	                -0.01297007, -0.00119088, 0.99991518]).reshape([3, 3])
	T = np.asarray([-0.0623, 0.0002, -0.0003]).reshape([3, 1])

	image_shape = (1280, 720)

	R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mat_L, dist_L, mat_R, dist_R, image_shape, R, T, alpha = 0)
	map1_1, map1_2 = cv2.initUndistortRectifyMap(mat_L, dist_L, R1, P1, image_shape, cv2.CV_16SC2)
	map2_1, map2_2 = cv2.initUndistortRectifyMap(mat_R, dist_R, R2, P2, image_shape, cv2.CV_16SC2)

	window_size = 3
	min_disp = 16
	num_disp = 100 - min_disp
	stereo = cv2.StereoSGBM_create(
		minDisparity = min_disp,
		numDisparities = num_disp,
		blockSize = 16,
		P1 = 8 * 3 * window_size ** 2,
		P2 = 32 * 3 * window_size ** 2,
		disp12MaxDiff = 1,
		uniquenessRatio = 8,
		speckleWindowSize = 80,
		speckleRange = 16,
		mode = cv2.STEREO_SGBM_MODE_HH,
	)

	cap_L = cv2.VideoCapture(0)
	cap_R = cv2.VideoCapture(3)

	if cap_L.isOpened() and cap_R.isOpened():
		print(">> cameras start ..")
	else:
		print(">> err, can not open camera ..")
		exit(-1)

	value_L = np.empty(2, object)
	value_R = np.empty(2, object)

	mix_image = False
	gray_mode = False

	loop = 1
	t0 = time.time()
	shot_frame = False
	folder_out = "/Users/kaismac/Downloads/stereo_camera/"
	folder_depth = mkdir(folder_out, "depth_sample")

	def process(img, head):
		if shot_frame: cv2.imwrite(folder_depth + head + f"{loop:05d}.jpg", img)
		if mix_image or gray_mode:
			img = cv2.resize(img, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
			img = cv2.fastNlMeansDenoisingColored(img, None, 4, 5, 5, 21)
			return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return img

	def func_L():
		ret, img = cap_L.read()
		if ret:
			img = cv2.remap(img[::-1, ::-1], map1_1, map1_2, cv2.INTER_CUBIC)
			img = process(img, "L")
		value_L[:] = ret, img

	def func_R():
		ret, img = cap_R.read()
		if ret:
			img = cv2.remap(img[::-1, ::-1], map2_1, map2_2, cv2.INTER_CUBIC)
			img = process(img, "R")
		value_R[:] = ret, img

	while True:
		staff_L = Thread(target = func_L)
		staff_R = Thread(target = func_R)
		staff_L.start()
		staff_R.start()
		staff_L.join()
		staff_R.join()
		if shot_frame: shot_frame = False
		key = cv2.waitKey(1)

		if value_L[0] and value_R[0]:
			img_l = value_L[1]
			img_r = value_R[1]
			if mix_image:
				disp = stereo.compute(img_l, img_r).astype(np.float32) / 16.0
				valid = disp > max(disp.min(), 0)

				depth_image = np.round(disp * (255 / disp.max()))
				depth_image[np.logical_not(valid)] = 0
				depth_image.astype(np.uint8)
				# depth_image = cv2.resize(depth_image, image_shape, interpolation = cv2.INTER_CUBIC)
				result = depth_image.astype(np.uint8)
				key = cv2.waitKey(0)
			elif gray_mode:
				gray = np.abs(np.asarray(img_l, np.int) - img_r)
				result = gray.astype(np.uint8)
				fig = KaisCanvas(fig_size = (10, 5.7), linewidth = 1, dark_mode = False)
				fig.histogram(np.ravel(gray), 2, force_delta = True, show_fit = False)
				fig.set_axis(equal_axis = False)
				path = folder_out + "hist_gray.png"
				fig.save(path)
				hist = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
				cv2.imshow("hist", hist)
			else:
				result = np.concatenate((img_l, img_r), axis = 1)[::2, ::4]
				result[25::56, :, 1] = 200
			cv2.imshow("cam", result)
		else: print(">> camera short circuit")

		if key == 27: break
		if key == ord("m"): mix_image = not mix_image
		if key == ord("s"): shot_frame = True
		if key == ord("g"): gray_mode = True

		fps = loop / (time.time() - t0)
		print(f"{loop}, fps = {fps:.1f}")
		loop += 1
	print(">> process finished ..")
	pass


if __name__ == '__main__':
	main()
	pass
