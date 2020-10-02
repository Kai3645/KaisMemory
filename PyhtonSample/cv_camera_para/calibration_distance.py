import cv2
import numpy as np
from tqdm import tqdm

from Core.Basic.KaisFunc import num2str
from Core.Basic.KaisPara import KaisPara
from Core.ComputerVision.camera_basic import camera_pose2checkboard
from Core.Math_geometry.geometry3d import fit_plane

if __name__ == '__main__':
	folder = KaisPara.iCloud + "Code/python/Sample/camera_basic/"
	folder_input = folder + "iPhone8/distance_input/"
	folder_output = folder + "iPhone8/distance_output/"

	name_format = "img - %d.png"
	idx_0 = 1
	z_real = np.arange(400, 1980, 30)
	cam_para = np.asarray((3375.31, 3375.31, 1981.55, 1472.71), np.float64)
	board_size = (9, 13)
	board_dx = 20.97

	total = len(z_real)
	z_calc = np.zeros(total)
	imgs = [cv2.imread(folder_input + name_format % i) for i in range(idx_0, idx_0 + total)]
	for i, img in enumerate(imgs):
		if img is not None: continue
		print("err input .. img %d" % i)
		exit(1)
	kappa = 0
	loop_control = 0
	while loop_control < 10:
		for i in tqdm(range(total), ">> calculating: "):
			pos, rot, _ = camera_pose2checkboard(
				src = imgs[i],
				camera_para = cam_para,
				board_size = board_size,
				board_r = board_dx,
				path_head = None,
				cam_F = 3.99,
			)
			z_calc[i] = pos[2]
		points = np.copy([z_real, z_calc]).transpose()
		A = fit_plane(points)
		kappa = -A[1] / A[0]
		print()
		print(f"loop {loop_control}, kappa = {kappa}")
		if abs(kappa - 1) < 4e-5: break
		cam_para[:2] = cam_para[:2] + cam_para[:2] * (kappa - 1) * 0.985
		print("fx, fy, cx, cy = " + num2str(cam_para, 2, separator = ", "))

	fw = open(folder_output + "_result.csv", "w")
	for i in tqdm(range(total), ">> calculating: "):
		pos, rot, mat = camera_pose2checkboard(
			src = imgs[i],
			camera_para = cam_para,
			board_size = board_size,
			board_r = board_dx,
			path_head = folder_output + "img_%03d_" % (i + idx_0),
			offset = (0, -130, 0),
			true_dis = False,
			cam_F = 3.99,
		)
		z_calc[i] = pos[2]
		fw.write(f"{i + idx_0}, {num2str(pos, 2)}, {num2str(rot, 1)}, {num2str(mat, 2)}\n")
	fw.close()
	print("fx, fy, cx, cy = " + num2str(cam_para, 2, separator = ", "))
	with open(folder_output + "/_calib.txt", "w") as fw:
		fw.write("fx, fy, cx, cy = " + num2str(cam_para, 2, separator = ", ") + "\n")
	pass
