import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from Core.Basic.KaisFigure import KaisFig2D
from Core.Math_geometry.CoordSystem import CoordSys
from Core.Math_geometry.geometry3d import fit_plane, plane_func

if __name__ == '__main__':
	lim = 10
	total = 2000
	points = (np.random.random((total, 3)) - 0.5) * [lim, lim, 1] * 2 + [0, 0, 1]
	mat = CoordSys.convMat((0, 0, 0), np.random.random(3) * math.pi * 2)
	points = CoordSys.conv(mat, points)

	K, flag_idx, order = fit_plane(points, with_flag_idx = True)
	print(K)
	print(order, flag_idx)

	# 3d plot raw data
	ax = Axes3D(plt.figure())

	x = points[:, 0]
	y = points[:, 1]
	z = points[:, 2]
	ax.scatter(x, y, z)

	block_count = 10
	lim_space = np.linspace(-lim * 0.8, lim * 0.8, block_count)

	X = np.zeros((3, block_count, block_count))
	X[order, :, :] = np.meshgrid(lim_space, lim_space)
	X[:, :, :] = plane_func(K, X, flag_idx)

	ax.plot_wireframe(X[0], X[1], X[2], color = "orchid")
	ax.set_xlim(-lim, lim)
	ax.set_ylim(-lim, lim)
	ax.set_zlim(-lim, lim)
	plt.show()

	# plot err
	t = np.arange(total)
	d = np.zeros(total)
	for i in range(total):
		d[i] = np.dot(points[i], K[:3]) + K[-1]
	fig = KaisFig2D()
	fig.plot(t, d)
	fig.Line((0, 0), (total, 0), color = "red", dashes = fig.dashes_01)
	fig.set_axis(ylim = (-lim, lim))
	fig.save("/Users/kaismbp/virtualenvs/myProject/output/out.png")

	pass
