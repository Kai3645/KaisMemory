import os

import cv2
import numpy as np
from tqdm import tqdm

from Core.Basic.KaisFunc import num2str
from Core.Basic.KaisPara import KaisPara
from Core.ComputerVision.camera_basic import calibration_digital_camera, camera_pose2checkboard

if __name__ == '__main__':
	folder = KaisPara.iCloud + "Code/python/Sample/camera_basic/"
	folder_input = folder + "iPhone8/calibrate_input/"
	folder_output = folder + "iPhone8/calibrate_output/"

	img_type = ".png"
	board_size = (9, 13)
	board_dx = 20.97

	paths = os.listdir(folder_input)
	imgs, names = [], []
	for p in tqdm(paths, desc = ">> scanning "):
		if img_type not in p: continue
		img = cv2.imread(folder_input + p)
		if img is None:
			print("can not read file " + p)
			exit(1)
		imgs.append(img)
		names.append(p.split(".")[0])

	cam_para = calibration_digital_camera(imgs, board_size, board_dx)
	with open(folder + "iPhone8/calibrate_output/_calib.txt", "w") as fw:
		fw.write("fx, fy, cx, cy = " + num2str(cam_para, 2, separator = ", ") + "\n")

	sum_dis, count = 0, 0
	fw = open(folder_output + "_dis.csv", "w")
	for i, name in enumerate(tqdm(names, ">> calculating: ")):
		pos, rot, cam_para = camera_pose2checkboard(
			src = imgs[i],
			camera_para = cam_para,
			board_size = board_size,
			board_r = board_dx,
			path_head = folder_output + name,
		)
		if pos is None: continue
		dis = np.linalg.norm(pos)
		sum_dis += dis
		count += 1
		fw.write(f"{name}, {num2str(pos, 4)}, {num2str(rot, 1)}, {dis:.2f}, {num2str(cam_para, 2)}\n")
	fw.close()
	print("fx, fy, cx, cy = " + num2str(cam_para, 2, separator = ", "))
	print(f"average dis = {sum_dis / count:.2f}")

	pass
