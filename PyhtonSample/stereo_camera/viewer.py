import time
from threading import Thread

import cv2
import numpy as np
from scipy.stats import stats

from Core.Basic import mkdir, err_exit


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
	resize_w = 640
	resize_h = 360
	resize_shape = (resize_w, resize_h)

	R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mat_L, dist_L, mat_R, dist_R, image_shape, R, T, alpha = 0)
	map1_1, map1_2 = cv2.initUndistortRectifyMap(mat_L, dist_L, R1, P1, image_shape, cv2.CV_16SC2)
	map2_1, map2_2 = cv2.initUndistortRectifyMap(mat_R, dist_R, R2, P2, image_shape, cv2.CV_16SC2)

	window_size = 5
	min_disp = 2
	depth_offset = 54
	num_disp = depth_offset - min_disp
	stereo = cv2.StereoSGBM_create(
		minDisparity = min_disp,
		numDisparities = num_disp,
		blockSize = 16,
		P1 = 8 * 3 * window_size ** 2,
		P2 = 32 * 3 * window_size ** 2,
		disp12MaxDiff = 1,
		uniquenessRatio = 10,
		speckleWindowSize = 100,
		speckleRange = 16,
		mode = cv2.STEREO_SGBM_MODE_HH,
	)

	value_L = np.empty(2, object)
	value_R = np.empty(2, object)
	gray_L_old = np.zeros((resize_h, resize_w), np.uint8)
	gray_R_old = np.zeros((resize_h, resize_w), np.uint8)

	mix_image = False
	gray_mode = False

	loop = 1
	shot_frame = False
	folder_out = "/Users/kaismac/Downloads/stereo_camera/"
	folder_depth = mkdir(folder_out, "depth_sample")

	gray_diff_th = 20
	CHANGE_RATIO = 0.2
	change_th = resize_w * resize_h * CHANGE_RATIO

	cap_L = cv2.VideoCapture(0)
	cap_R = cv2.VideoCapture(3)
	if cap_L.isOpened() and cap_R.isOpened(): print(">> cameras start ..")
	else: err_exit(">> err, can not open camera ..")

	def process(img, head, gray_old):
		if shot_frame: cv2.imwrite(folder_depth + head + f"{loop:05d}.jpg", img)
		img = cv2.resize(img, resize_shape, interpolation = cv2.INTER_LINEAR)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.medianBlur(gray, 3)
		if mix_image:
			diff = cv2.absdiff(gray, gray_old)
			th = stats.mode(diff, axis = None)[0][0]
			diff_valid = diff > th + gray_diff_th
			if gray_mode:
				diff[np.logical_not(diff_valid)] = 0
				return diff, gray

			if np.sum(diff_valid) > change_th: return None, gray
			return gray, gray
		elif gray_mode: return gray, gray
		return img, gray

	def func_L():
		ret, img = cap_L.read()
		if ret:
			img = cv2.remap(img[::-1, ::-1], map1_1, map1_2, cv2.INTER_CUBIC)
			img, gray = process(img, "L", gray_L_old)
			gray_L_old[:, :] = gray
		value_L[:] = ret, img

	def func_R():
		ret, img = cap_R.read()
		if ret:
			img = cv2.remap(img[::-1, ::-1], map2_1, map2_2, cv2.INTER_CUBIC)
			img, gray = process(img, "R", gray_R_old)
			gray_R_old[:, :] = gray
		value_R[:] = ret, img

	t_ = time.time()
	result = np.zeros((resize_h, resize_w, 3), np.uint8)
	while True:
		cv2.imshow("stereo", result)
		key = cv2.waitKey(1)
		if key == 27: break
		if key == ord("s"): shot_frame = True
		if key == ord("m"): mix_image = not mix_image
		if key == ord("g"): gray_mode = not gray_mode
		if key == ord("["): gray_diff_th = max(1, gray_diff_th - 1)
		if key == ord("]"): gray_diff_th = min(50, gray_diff_th + 1)

		staff_L = Thread(target = func_L)
		staff_R = Thread(target = func_R)
		staff_L.start()
		staff_R.start()
		staff_L.join()
		staff_R.join()
		if shot_frame: shot_frame = False

		ti = time.time()
		fps = 1 / (ti - t_)
		t_ = ti
		print(f"{loop}, fps = {fps:.1f}")
		buffer_old = result
		loop += 1

		if not value_L[0] or not value_R[0]:
			print(">> camera short circuit")
			continue
		if value_L[1] is None:
			result = buffer_old
			continue
		if value_R[1] is None:
			result = buffer_old
			continue

		img_l = value_L[1]
		img_r = value_R[1]

		if mix_image:
			if gray_mode:
				img_l = cv2.cvtColor(img_l, cv2.COLOR_GRAY2BGR)
				img_r = cv2.cvtColor(img_r, cv2.COLOR_GRAY2BGR)
			else:
				disp = stereo.compute(img_l, img_r).astype(np.float32) / 16.0
				valid = disp > max(disp.min(), 0)

				depth_image = np.round(disp * (255 / disp.max())).astype(np.uint8)
				depth_image[np.logical_not(valid)] = 0
				result = cv2.resize(depth_image[:, depth_offset:], resize_shape, interpolation = cv2.INTER_CUBIC)
				continue
		elif gray_mode:
			gray_diff = cv2.absdiff(img_l, img_r)
			diff_th = stats.mode(gray_diff, axis = None)[0][0]
			max_gary = diff_th + gray_diff_th
			gray_diff = gray_diff.astype(np.float32)
			gray_diff[gray_diff > max_gary] = 0
			gray_diff *= 250 / max_gary
			result = gray_diff.astype(np.uint8)
			continue

		result = np.concatenate((img_l, img_r), axis = 1)[::, ::2]
		result[25::56, :, 1] = 100
	print(">> process finished ..")
	pass


if __name__ == '__main__':
	main()
	pass
