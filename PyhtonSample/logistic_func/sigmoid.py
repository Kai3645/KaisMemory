import math

import numpy as np
import matplotlib.pyplot as plt

from A_core.A_01_para import KaisPara


def sigmoid(x, a):
	x *= a
	s = 1 / (1 + math.e ** -x)
	return s


def main():
	count = 100
	np.random.seed(0)
	x = np.random.randn(count)
	x_lim_1 = int(min(x)) - 2
	x_lim_2 = int(max(x)) + 2
	x.sort()
	y = np.arange(0, 1, 1 / count)
	plt.scatter(x, y,
	            marker = "x", s = 18, color = "chocolate",
	            linewidths = 0.4, edgecolors = "black")

	x = np.arange(x_lim_1, x_lim_2, 0.01)
	y = sigmoid(x,1)

	plt.plot(x, y, linewidth = 1)
	plt.savefig(f_out + "img.png", dpi = 300)
	plt.close()


if __name__ == '__main__':
	f_out = KaisPara.f_code + "X_support/logistic_func/output/"
	main()
