import time

import cv2
import numpy as np
from tqdm import tqdm

from Core.Basic import listdir, err_exit, num2str, mkdir
from Core.ComputerVision.camera_basic import chessboard_corner_3d, chessboard_corner_detect
from Core.ComputerVision.image_basic import gray2binary

if __name__ == '__main__':
	folder_out = "/home/kai/PycharmProjects/pyCenter/diary_output/d_20210507/"
	BOARD_R = 0.04231
	BOARD_W = 8
	BOARD_H = 5
	IMAGE_W = 1280
	IMAGE_H = 720
	board_shape = (BOARD_W, BOARD_H)
	image_shape = (IMAGE_W, IMAGE_H)
	CHANGE_RATIO = 0.1
	change_th = IMAGE_W * IMAGE_H * CHANGE_RATIO
	do_rotate_image = True

	mat_L = np.asarray([373.2465, 0, 626.9151, 0, 373.3987, 363.1092, 0, 0, 1]).reshape((3, 3))
	mat_R = np.asarray([370.7673, 0, 603.3985, 0, 370.6573, 349.1074, 0, 0, 1]).reshape((3, 3))
	dist_L = np.asarray([2.50764566, 3.69586221, 0.00208109, 0.00235887,
	                     0.05245894, 2.22065863, 3.17493684, 0.34092975,
	                     -0.00070810, -0.00030914, -0.00230941, -0.00007401,
	                     -0.00423250, 0.00819843])
	dist_R = np.asarray([2.85760726, 4.60387629, 0.00014143, 0.00221237,
	                     0.06523993, 2.58364108, 3.89364134, 0.42966194,
	                     -0.00247370, 0.00001714, -0.00042481, -0.00004474,
	                     0.00310306, 0.00342365])

	time_start = time.time()

	# collect images paths
	imgs_path_L = "/mnt/DATA_SSD/Sample_Dataset/stereo_camera/LCam/"
	imgs_path_R = "/mnt/DATA_SSD/Sample_Dataset/stereo_camera/RCam/"
	img_names_L = listdir(imgs_path_L)
	img_names_R = listdir(imgs_path_R)


	def corner_det(path, binary_old):
		img = cv2.imread(path)
		if do_rotate_image: img = img[::-1, ::-1]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		binary = gray2binary(gray)

		diff_valid = binary_old != binary
		if np.sum(diff_valid) < change_th: return False, binary_old, None

		corners = chessboard_corner_detect(gray, board_shape, binary)
		if corners is None: return False, binary_old, None
		return True, binary, corners


	img_corners_L, img_corners_R = [], []
	binary_old_l = np.zeros((IMAGE_H, IMAGE_W), np.uint8)
	binary_old_r = np.zeros((IMAGE_H, IMAGE_W), np.uint8)

	for n_l, n_r in tqdm(zip(img_names_L, img_names_R), total = len(img_names_L), desc = ">> scanning "):
		if n_l[1:] != n_r[1:]: err_exit(n_l + " =/= " + n_r + ", name match err ..")

		flag, binary_l, corners_l = corner_det(imgs_path_L + n_l, binary_old_l)
		if not flag: continue
		flag, binary_r, corners_r = corner_det(imgs_path_R + n_r, binary_old_r)
		if not flag: continue

		img_corners_L.append(corners_l)
		img_corners_R.append(corners_r)
		binary_old_l = binary_l
		binary_old_r = binary_r
	img_corners_L = np.asarray(img_corners_L)
	img_corners_R = np.asarray(img_corners_R)

	test_num = -1
	CALIB_MAX_ABILITY = 250
	CALIB_MIN_IMAGE_NUM = 40
	if test_num < 0: test_num = CALIB_MAX_ABILITY
	else: test_num = min(test_num, CALIB_MAX_ABILITY)

	working_corners_L = img_corners_L
	working_corners_R = img_corners_R
	frame_count = len(img_corners_L)
	if frame_count < CALIB_MIN_IMAGE_NUM:
		err_exit(">> err, need more good chessboard images .. ")
	if frame_count > test_num:
		indexes = np.arange(test_num) / test_num
		indexes = (indexes * frame_count).astype(int)
		working_corners_L = img_corners_L[indexes]
		working_corners_R = img_corners_R[indexes]
		frame_count = test_num

	corners_3d = chessboard_corner_3d(BOARD_W, BOARD_H, BOARD_R)
	object_points = np.tile(corners_3d, (frame_count, 1, 1))

	_, mat_L, dist_L, mat_R, dist_R, R, T, _, _ = cv2.stereoCalibrate(
		object_points, working_corners_L, working_corners_R,
		mat_L, dist_L, mat_R, dist_R, image_shape, flags = (
			cv2.CALIB_USE_INTRINSIC_GUESS |
			cv2.CALIB_RATIONAL_MODEL |
			cv2.CALIB_TILTED_MODEL |
			cv2.CALIB_THIN_PRISM_MODEL
		)
	)

	fw = open(folder_out + "stereo_calib_result.txt", "w")
	fw.write("L distCoeffs = \n\t" + num2str(dist_L, 8) + "\n")
	fw.write("L camera mat = \n\t" + num2str(mat_L, 4) + "\n")
	fw.write("R distCoeffs = \n\t" + num2str(dist_R, 8) + "\n")
	fw.write("R camera mat = \n\t" + num2str(mat_R, 4) + "\n")
	fw.write("R = \n\t" + num2str(R, 8) + "\n")
	fw.write("T = \n\t" + num2str(T, 4) + "\n")
	fw.close()

	print("===============================")
	print("R = ")
	print(R)
	print("- - - - - - - - - - - - - - - -")
	print("T = ")
	print(T)
	print("===============================")

	R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mat_L, dist_L, mat_R, dist_R, image_shape, R, T, alpha = 1)
	map1_1, map1_2 = cv2.initUndistortRectifyMap(mat_L, dist_L, R1, P1, image_shape, cv2.CV_16SC2)
	map2_1, map2_2 = cv2.initUndistortRectifyMap(mat_R, dist_R, R2, P2, image_shape, cv2.CV_16SC2)

	folder_stereo = mkdir(folder_out, "stereo")
	for i in tqdm(range(len(img_names_L)), desc = ">> undistort "):
		img1 = cv2.imread(imgs_path_L + img_names_L[i])[::-1, ::-1]
		img2 = cv2.imread(imgs_path_R + img_names_R[i])[::-1, ::-1]
		result1 = cv2.remap(img1, map1_1, map1_2, cv2.INTER_CUBIC)
		result2 = cv2.remap(img2, map2_1, map2_2, cv2.INTER_CUBIC)
		result = np.concatenate((result1[:, ::3], result2[:, ::3]), axis = 1)
		result[13::27, :, 1] = 150
		cv2.imwrite(folder_stereo + f"{i:05d}.jpg", result)
	time_used = time.time() - time_start
	print(f">> process finished, time used = {time_used:.2f} s .. ")
