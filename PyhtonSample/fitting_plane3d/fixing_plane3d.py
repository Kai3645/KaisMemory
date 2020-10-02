import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tqdm import tqdm

from A_src.T_las_road.A_RoadPoints import RoadP
from Core.Basic.KaisFigure import KaisFig2D
from Core.Math_geometry.CoordSystem import CoordSys
from Core.Math_geometry.geometry3d import fit_plane, plane_func

if __name__ == '__main__':
	lim = 10
	total = 4000
	np.random.seed(0)
	points = (np.random.random((total, 3)) - 0.5) * [lim, lim, 0.1] * 2 + [0, 0, 1]
	mat = CoordSys.convMat((0, 0, 0), np.random.random(3) * math.pi * 2)
	points = CoordSys.conv(mat, points)

	K, flag_idx, order = fit_plane(points, with_flag_idx = True)

	# plot err
	# fig = KaisFig2D(fig_size = (21, 5), dpi = 200)
	# t = np.arange(total)

	d = np.zeros(total)
	for i in range(total):
		d[i] = np.dot(points[i], K[:3]) + K[-1]
	print("Err = %.6f" % np.sqrt(np.dot(d, d)))
	# fig.plot(t, d, zorder = 10)

	# print(K)
	# print(order, flag_idx)

	rp = RoadP(points)
	dst = np.zeros((total, 3))
	for i, pos in enumerate(tqdm(points)):
		dst[i, :] = rp.plane_inter(pos)

	for i in range(total):
		d[i] = np.dot(dst[i], K[:3]) + K[-1]
	print("Err = %.6f" % np.sqrt(np.dot(d, d)))
	# fig.plot(t, d, zorder = 12)

	# 3d plot raw data
	ax = Axes3D(plt.figure())

	ax.scatter(points[:, 0], points[:, 1], points[:, 2])
	ax.scatter(dst[:, 0], dst[:, 1], dst[:, 2])

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

	# fig.Line((0, 0), (total, 0), color = "red", dashes = fig.dashes_01, zorder = 5)
	# fig.set_axis()
	# fig.save("/Users/kaismbp/virtualenvs/myProject/output/out.png")

	pass
