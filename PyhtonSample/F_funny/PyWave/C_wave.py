import cv2
import numpy as np

from A_core.B_01_KaisColor import KaisColor


class Wave:
	def __init__(self, **keywords):
		self.bit_size = keywords.get("bit_size", (80, 120))
		self.img_size = keywords.get("img_size", (720, 480))
		self.grid_size = (self.img_size[1], self.img_size[0])
		self.img_shape = (self.img_size[1], self.img_size[0], 3)

		self.color_dig = keywords.get("color_dig", 500)
		self.colors = KaisColor.plotColorMap("hot", self.color_dig + 1)

		K = keywords.get("K", 0.5)
		a0 = 2 - K * 4 + K * K * 2 / 3
		a1 = K - K * K / 3
		a2 = K * K / 6
		self.kernel = np.asarray([
			[a2, a1, a2],
			[a1, a0, a1],
			[a2, a1, a2],
		], np.float64)

		self.dampening = keywords.get("dampening", 1.0)

		self.grid_0 = np.zeros(self.grid_size)
		self.grid_1 = np.zeros(self.grid_size)
		self.lim_min = 0
		self.lim_max = 0
		self.reset()
		pass

	def reset(self):
		sub_grid = np.random.random(self.bit_size) * self.color_dig
		gray = np.round(sub_grid).astype(np.uint16)

		self.grid_0 = np.zeros(self.grid_size)
		self.grid_1[:, :] = cv2.resize(
				gray, self.img_size,
				interpolation = cv2.INTER_LANCZOS4
		) / self.color_dig - 0.5
		self.grid_1 *= 50

		for i in range(10):
			self.update()

		self.lim_min = np.min(self.grid_1)
		self.lim_max = np.max(self.grid_1)

		pass

	def update(self):
		grid_2 = cv2.filter2D(
				self.grid_1, -1, self.kernel,
				borderType = cv2.BORDER_CONSTANT
		) - self.grid_0
		grid_2 *= self.dampening

		tmp_min = np.min(grid_2)
		tmp_max = np.max(grid_2)
		# print("min = %.2f" % tmp_min, end = ", ")
		# print("max = %.2f" % tmp_max, end = ", ")

		limit_num = 100
		tmp_min -= self.lim_min
		if tmp_min < -limit_num: self.lim_min -= 1
		elif tmp_min > limit_num: self.lim_min += 1

		tmp_max -= self.lim_max
		if tmp_max < -limit_num: self.lim_max -= 1
		elif tmp_max > limit_num: self.lim_max += 1

		# print("min = %d" % self.lim_min, end = ", ")
		# print("max = %d" % self.lim_max)

		self.grid_0 = self.grid_1
		self.grid_1 = grid_2
		pass

	def push_img(self):
		a = self.lim_min
		b = self.lim_max - a

		idx = (self.grid_1 - a) / b * self.color_dig
		idx[np.where(idx < 0)] = 0
		idx = np.round(idx).astype(np.uint16)
		idx[np.where(idx > self.color_dig)] = self.color_dig

		img = np.zeros(self.img_shape, np.uint8)
		img[:, :, :] = self.colors[idx[:, :]]

		return img

	def C_push_ripple(self, pos):
		a = max(0, pos[1] - 3)
		b = min(self.img_size[1], pos[1] + 3)
		c = max(0, pos[0] - 3)
		d = min(self.img_size[0], pos[0] + 3)
		self.grid_1[a:b, c:d] += 100
