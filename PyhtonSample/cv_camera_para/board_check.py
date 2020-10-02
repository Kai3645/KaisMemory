import os

import cv2
from tqdm import tqdm

from Core.Basic.KaisPara import KaisPara
from Core.ComputerVision.camera_basic import checkboard_corner_detect, draw_board_corners

if __name__ == '__main__':
	folder = KaisPara.iCloud + "Code/python/Sample/camera_basic/"
	folder_input = folder + "iPhone8/calibrate_input/"
	# folder_input = folder + "iPhone8/distance_input/"
	folder_output = folder + "iPhone8/tmp/"

	img_type = ".png"
	board_size = (9, 13)

	paths = os.listdir(folder_input)
	for p in tqdm(paths, desc = ">> scanning "):
		if img_type not in p: continue
		img = cv2.imread(folder_input + p)
		if img is None:
			print("can not read file " + p)
			continue
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		uvn = checkboard_corner_detect(gray, board_size)
		if uvn is None:
			print("can not find checkboard " + p)
			continue
		name = p.split(".")[0]
		draw_board_corners(img, uvn, folder_output + name + ".jpg", )
	pass
