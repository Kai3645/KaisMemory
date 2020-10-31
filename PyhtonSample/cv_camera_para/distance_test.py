import os

import cv2
import numpy as np
from tqdm import tqdm

from Core.Basic.KaisFunc import num2str
from Core.Basic.KaisPara import KaisPara
from Core.ComputerVision.camera_basic import pose2checkboard_digCamera

if __name__ == '__main__':
	folder = KaisPara.iCloud + "Code/python/Sample/camera_basic/"
	folder_input = folder + "iPhone8/sample/"
	folder_output = folder + "iPhone8/sample/"

	img_type = ".png"
	board_size = (9, 13)
	board_dx = 20.97
	cam_para = np.asarray((3271.85, 3271.85, 1981.55, 1472.71), np.float64)

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

	fw = open(folder_output + "_dis.csv", "w")
	for i, name in enumerate(tqdm(names, ">> calculating: ")):
		pos, rot, mat = pose2checkboard_digCamera(
			src = imgs[i],
			camera_para = cam_para,
			board_size = board_size,
			board_r = board_dx,
			path_head = folder_output + name,
			offset = (0, -5 * board_dx, 0),
			cam_F = 3.99,
			true_dis = True,
		)
		if pos is None: continue
		dis = np.linalg.norm(pos)
		fw.write(f"{name}, {num2str(pos, 4)}, {num2str(rot, 1)}, {dis:.2f}, {num2str(mat, 2)}\n")
	fw.close()
