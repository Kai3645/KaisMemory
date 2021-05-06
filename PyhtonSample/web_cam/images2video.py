import cv2
from tqdm import tqdm

from Core.Basic import listdir, str2folder

if __name__ == '__main__':
	folder = str2folder("/Users/kaismac/Downloads/time_lapse")

	names = listdir(folder, pattern = "*.jpg")
	out = cv2.VideoWriter(
		'/Users/kaismac/Downloads/out.mov', apiPreference = cv2.CAP_ANY,
		fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps = 60, frameSize = (1200, 675),
	)  # 861030210
	for n in tqdm(names[300:]):
		img = cv2.imread(folder + n)
		out.write(img)
	pass
