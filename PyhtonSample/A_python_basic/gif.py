import cv2
# import imageio
import numpy as np

from A_core.B_01_KaisColor import KaisColor


# def create_gif(imgs, path, **keywords):
# 	imageio.mimsave(path, imgs, 'GIF', **keywords)
# 	return None


def update(grid_0, grid_1, kernel):
	tmp = cv2.filter2D(grid_1, -1, kernel, borderType = cv2.BORDER_CONSTANT)
	tmp -= grid_0
	tmp *= 0.999
	print(np.min(tmp), np.max(tmp))
	return tmp


def main():
	K = 0.002
	a0 = 2 - K * 4 + K * K * 2 / 3
	a1 = K - K * K / 3
	a2 = K * K / 6
	kernel = np.asarray([
		[a2, a1, a2],
		[a1, a0, a1],
		[a2, a1, a2],
	], np.float64)

	# img_size = (70, 105)
	img_size = (28, 41)
	grid_0 = np.zeros(img_size)
	grid_1 = np.random.random(img_size) - 0.5
	for i in range(100):
		grid_2 = update(grid_0, grid_1, kernel)
		grid_0 = grid_1
		grid_1 = grid_2

	cmap = "hot"
	imgs = []
	# colors = KaisColor.plotColorMap(cmap, 120 + 400 + 1)[120:]
	for i in range(600):
		print(i, end = ", ")

		grid_2 = update(grid_0, grid_1, kernel)
		grid_0 = grid_1
		grid_1 = grid_2

		# idx = (np.copy(grid_2) + 16) / 8 * 400
		# idx[np.where(idx < 0)] = 0
		# idx = np.round(idx).astype(np.uint16)
		# idx = cv2.resize(idx, (1080, 720), interpolation = cv2.INTER_LANCZOS4)
		# idx[np.where(idx < 600)] = 600
		# idx[np.where(idx > 1000)] = 1000
		# idx -= 600

		# img = np.zeros((720, 1080, 3), np.uint8)
		# img[:, :, :] = colors[idx[:, :]]

		# imgs.append(img[:, :])
		# pass

	# create_gif(imgs, f_out + cmap + ".gif", fps = 30)
	pass


if __name__ == '__main__':
	f_out = "/Users/kaismbp/virtualenvs/myProject/output/"

	main()
