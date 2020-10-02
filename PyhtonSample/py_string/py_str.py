import numpy as np

from Core.Basic.KaisFunc import rand_str
from Core.Basic.KaisTest import KaisTest


def slicer_compare():
	def slicer_01(a, start: int, end: int):
		a = np.asarray(a)
		s0 = a.shape

		a = a.ravel()
		s1 = np.append(a.shape, -1)

		a = a.view((str, 1)).reshape(s1)[:, start:end].tostring()
		return np.frombuffer(a, (str, end - start)).reshape(s0)

	def slicer_02(a, start: int, end: int):
		a = np.asarray(a)
		s0 = a.shape

		a = a.ravel()
		s1 = np.append(a.shape, -1)

		a = a.view((str, 1)).reshape(s1)[:, start:end].ravel()
		return a.view((str, end - start)).reshape(s0)

	def slicer_03(a, start: int, end: int):
		a = np.asarray(a)
		s = a.shape

		a = np.asarray([i[start:end] for i in a.ravel()])
		return a.reshape(s)

	def slicer_04(a, start: int, end: int):
		return np.frompyfunc(lambda x: x[start:end], 1, 1)(a)

	ask = rand_str(10, (1000, 200))
	kwargs = dict()

	KaisTest.func_speed(
		funcs = [
			slicer_01,
			slicer_02,
			slicer_03,
			slicer_04,
		],
		names = [
			"slicer_01",
			"slicer_02",
			"slicer_03",
			"slicer_04",
		],
		repeat = 10,
		args = (
			ask, 2, 5,
		), **kwargs
	)
