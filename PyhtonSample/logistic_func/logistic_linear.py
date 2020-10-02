import numpy as np
import matplotlib.pyplot as plt

from A_core.A_01_para import KaisPara


def main():
	count = 20
	X = np.random.randn(count)
	X.sort()
	Y = np.arange(0, count, 1)
	plt.scatter(X, Y)
	plt.savefig(f_out + "img.png", dpi = 300)
	plt.close()

	pass


if __name__ == '__main__':
	f_out = KaisPara.f_code + "X_support/logistic_func/output/"
	main()
