import os

import cv2
import numpy as np
from tqdm import tqdm

from Core.Basic.KaisLog import err_exit
from Core.Basic.KaisPara import KaisPara
from Core.ComputerVision.merge_image import stitching

if __name__ == '__main__':
	main_folder = KaisPara.Python + "Sample/cv_image_merge/"
	folder_input = main_folder + "sample/case_02/"
	folder_output = main_folder + "tmp/case_02/"

	img_type = ".jpg"
	paths = os.listdir(folder_input)
	src_images = []
	for f in tqdm(paths, desc = ">> scanning "):
		if img_type not in f: continue
		image = cv2.imread(folder_input + f)
		if image is None: err_exit(f"can not read image {f} .. ")
		src_images.append(image[600:1770, 1400:2900])
	src_images = np.asarray(src_images)

	dst = stitching(
		src_imgs = src_images,
		folder = folder_output,
		work_pix = 1, seam_pix = 1,
		feature_type = "surf",
		work_inter = "linear",
		ba_cost_type = "reproj",
		ba_refine_mask = "ynyny",
		wave_correct = "horiz",
		warp_type = "plane",
		comp_type = "gain_blocks",
		comp_block_size = 40,
		comp_num_filter = 2,
		blend_type = "multiband",
		blend_inter = "cubic",
		blend_strength = 20,
	)
	if dst is None: err_exit(f"can not stitching image .. ")
	cv2.imwrite(folder_output + "result.jpg", dst)
