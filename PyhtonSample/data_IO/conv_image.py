import cv2
from tqdm import tqdm

from Core.Basic.LogFunc import listdir, mkdir

if __name__ == '__main__':
	folder = "/home/kai/PycharmProjects/pyCenter/diary_output/d_20201030/"
	names = listdir(folder)
	f_out = mkdir("/home/kai/PycharmProjects/pyCenter/diary_output", "d_20201031")
	for n in tqdm(names):
		img = cv2.imread(folder + n)
		cv2.imwrite(f_out + n[:-4] + ".png", img)
	pass
