import cv2
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from Core.Basic.LogFunc import err_exit, mkdir, listdir


def __pipeline(video_path, folder_out):
	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened(): err_exit(f"err, can not open video, @\"{video_path}\"")

	total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	dts = np.zeros(total)

	t_old = t0 = 0
	for i in tqdm(range(total)):
		ret, frame = cap.read()
		if not ret: break
		ti = t0 + cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
		dts[i] = ti - t_old
		t_old = ti

		cv2.imwrite(folder_out + f"img_{i:04d}.jpg", frame)

	plt.plot(dts[1:])
	plt.savefig(folder_out + "ana.pdf")
	plt.close()
	pass


if __name__ == '__main__':
	f_out = "/home/kai/PycharmProjects/pyCenter/diary_output/d_20201029/"
	f_in = "/home/kai/Documents/MELCO/temp_cam/"
	names = listdir(f_in)
	for index, n in enumerate(names):
		if ".mp4" not in n: continue
		print(f"{index} -> unzip {n}")
		__pipeline(
			video_path = f_in + n,
			folder_out = mkdir(f_out, f"v_{index:03d}"),
		)
		pass
	pass
