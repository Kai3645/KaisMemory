import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay

from Core.Geometry import is_CCW_2d


def main():
	points = np.random.randint(0, 100, (10, 2))

	tri = Delaunay(points)

	simplices = []
	tri.simplices.sort(axis = 1)
	# tri.simplices.sort(axis = 0)
	for idx in tri.simplices:
		P3 = points[idx]
		if not is_CCW_2d(P3): continue
		simplices.append(idx)

	plt.triplot(points[:, 0], points[:, 1], tri.simplices, zorder = 10)
	plt.triplot(points[:, 0], points[:, 1], simplices, zorder = 12)
	plt.plot(points[:, 0], points[:, 1], 'o', zorder = 14)
	plt.show()


if __name__ == '__main__':
	main()
