import numpy as np
import matplotlib.pyplot as plt

from A_core.A_01_para import KaisPara


def main():
	mu, sigma = 0, .2
	s = np.random.normal(loc = mu, scale = sigma, size = 10000)
	plt.hist(s, 50, density = True, zorder = 10)

	t = np.arange(-4 * sigma, 4 * sigma, 0.01)
	plt.plot(t, 1 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-(t - mu) ** 2 / (2 * sigma ** 2)),
	         linewidth = 1, c = "crimson", alpha = 0.9, zorder = 12)

	mu = np.mean(s)
	sigma = np.std(s, ddof = 1)

	plt.plot(t, 1 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-(t - mu) ** 2 / (2 * sigma ** 2)),
	         linewidth = 1, c = "crimson", alpha = 0.9, zorder = 14)

	plt.savefig(f_out + "img.png", dpi = 300)


if __name__ == '__main__':
	f_out = KaisPara.f_code + "X_support/normal_distribution/output/"
	main()
