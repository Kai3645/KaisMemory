import numpy as np
import matplotlib.pyplot as plt

from A_core.A_02_func import KaisFunc


def sigmoid(x, w):
	y = x * w[0] + w[1]
	return 1 / (1 + np.exp(-y))


def make_data(length):
	data = np.zeros((length, 2))
	half = length // 2
	data[:half, 0] = np.random.normal(-2, 0.5, half)
	data[half:, 0] = np.random.normal(2, 0.65, half)
	data[half:, 1] = 1

	fw = open("/Users/kaismbp/virtualenvs/myProject/output/data.csv", "w")
	for x, z in data:
		fw.write("%.6f,%d\n" % (x, z))
	fw.close()


def read_data():
	path = "/Users/kaismbp/virtualenvs/myProject/output/data.csv"
	length = KaisFunc.fileLength(path)
	data = np.zeros((length, 2))

	fr = open(path, "r")
	for i, line in enumerate(fr):
		row = line.split(",")
		data[i, :] = np.float64(row)
	fr.close()
	return data


def main():
	data = read_data()

	# data = np.array([
	# 	[1.20, 0], [1.25, 0], [1.30, 0],
	# 	[1.35, 0], [1.40, 1], [1.45, 0],
	# 	[1.50, 1], [1.55, 0], [1.60, 1],
	# 	[1.65, 1], [1.70, 1], [1.75, 1]
	# ], np.float64)

	x = data[:, 0]
	z0 = data[:, 1]

	p = 0.9
	e = 1e-3
	g = np.zeros(2)
	w = np.asarray([1, -np.average(x)], np.float64)

	err0 = 0
	T = np.linspace(min(x), max(x), 1000)
	for count in range(100000):
		# for i in range(len(data)):
		# zi = sigmoid(x[i], w)
		# k = (zi - z0[i]) * zi * (1 - zi)
		# dw = np.asarray([k * x[i], k], np.float64)
		# g = p * g + (1 - p) * dw * dw
		# w = w - 0.1 / np.sqrt(g + e) * dw

		z = sigmoid(x, w)
		k = (z - z0) * z * (1 - z)
		dw = np.asarray([k * x, k]).transpose()
		g = p * g + (1 - p) * np.average(dw * dw, axis = 0)
		w = w - np.average(dw, axis = 0) / np.sqrt(g + e)
		w = np.round(w, 8)

		z = sigmoid(x, w)
		err = np.sqrt(np.dot(z - z0, z - z0))
		if abs(err - err0) < 1e-6:
			print(">> final =", count, w, abs(err - err0))
			break
		if count % 500 == 1:
			plt.plot(T, sigmoid(T, w), color = "y")
			print(count, w, abs(err - err0))
		err0 = err

	plt.plot(T, sigmoid(T, w))
	plt.plot(data[:, 0], data[:, 1], "ro", markersize = 3)
	plt.show()

	fw = open("/Users/kaismbp/virtualenvs/myProject/output/result.csv", "w")
	z1 = sigmoid(x, w)
	for xi, z0i, z1i in zip(x, z0, z1):
		fw.write("%.6f,%d,%.6f\n" % (xi, z0i, z1i))
	fw.close()


if __name__ == '__main__':
	make_data(10000)
	main()
	pass
