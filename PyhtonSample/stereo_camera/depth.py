import cv2
import numpy as np
from tqdm import tqdm

from Core.Basic import listdir
from Core.Visualization import PCModel

if __name__ == '__main__':
	mat_L = np.asarray([371.7238, 0.0000, 603.0837, 0.0000, 371.6990, 349.0501, 0.0000, 0.0000, 1.0000]).reshape([3, 3])
	mat_R = np.asarray([372.4407, 0.0000, 626.7559, 0.0000, 372.5443, 362.9187, 0.0000, 0.0000, 1.0000]).reshape([3, 3])
	dist_L = np.asarray([2.58339740, 4.27790321, -0.00000468, 0.00133856, 0.04181726, 2.31375616, 3.64480336,
	                     0.37388115, -0.00173613, 0.00014957, -0.00010390, -0.00005456, 0.00259686, 0.00150627])
	dist_R = np.asarray([2.85419397, 4.41270687, 0.00016594, 0.00290789, 0.07042960, 2.57469084, 3.74501496,
	                     0.42086447, -0.00147710, -0.00023769, -0.00066186, 0.00004257, 0.00026240, 0.01072015])
	R = np.asarray([0.99990214, 0.00522852, 0.01297612, -0.00524353, 0.99998562,
	                0.00112295, -0.01297007, -0.00119088, 0.99991518]).reshape([3, 3])
	T = np.asarray([-0.0623, 0.0002, -0.0003]).reshape([3, 1])

	image_shape = (1280, 720)

	R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mat_L, dist_L, mat_R, dist_R, image_shape, R, T, alpha = 0)
	print(Q)
	# map1_1, map1_2 = cv2.initUndistortRectifyMap(mat_L, dist_L, R1, P1, image_shape, cv2.CV_16SC2)
	# map2_1, map2_2 = cv2.initUndistortRectifyMap(mat_R, dist_R, R2, P2, image_shape, cv2.CV_16SC2)

	folder_input = "/mnt/DATA_SSD/Sample_Dataset/stereo_camera/depth_sample/"
	img_names_L = listdir(folder_input, pattern = "L*.jpg")
	img_names_R = listdir(folder_input, pattern = "R*.jpg")

	folder_out = "/home/kai/PycharmProjects/pyCenter/diary_output/d_20210507/depth/"

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

	for i in tqdm(range(len(img_names_L)), desc = ">> undistort "):
		img1 = cv2.imread(folder_input + img_names_L[i], cv2.IMREAD_GRAYSCALE)
		img1 = cv2.fastNlMeansDenoising(img1, None, 4, 5, 23)
		img2 = cv2.imread(folder_input + img_names_R[i], cv2.IMREAD_GRAYSCALE)
		img2 = cv2.fastNlMeansDenoising(img2, None, 4, 5, 23)

		disp = stereo.compute(img1, img2).astype(np.float32) / 16.0
		valid = disp > max(disp.min(), 0)

		depth_image = np.round(disp * (255 / disp.max()))
		depth_image[np.logical_not(valid)] = 0
		depth_image.astype(np.uint8)
		depth_image = cv2.resize(depth_image, image_shape, interpolation = cv2.INTER_CUBIC)
		cv2.imwrite(folder_out + f"{i:05d}.jpg", depth_image)

		points = cv2.reprojectImageTo3D(disp, Q)
		colors = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
		model = PCModel()
		model.add_point(points[valid], colors[valid])
		model.save_to_las(folder_out + f"{i:05d}.las")
	pass
