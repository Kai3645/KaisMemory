import math

import numpy as np
from vispy import app, scene

from Core.Basic import err_exit
from Core.Math import unwrap_angle
from Core.Visualization import PCModel, KaisColor

if __name__ == '__main__':
	def main():
		R = 5.0
		V = 1.0
		K = 4.0

		# (dis, angle)
		A = np.asarray([0, 0])
		B = np.asarray([R, math.pi])
		r = max(0.0, 1 - math.pi / K) * R
		if K * r >= R: err_exit("bad, case")

		t = 0
		dt = 0.0001
		Vdt = V * dt
		wdt = K * Vdt / R

		def fA(Ai, Bi):
			if Ai[0] >= r: return Ai + (Vdt, 0)
			if Ai[0] <= 0: return np.asarray([Vdt, unwrap_angle(Bi[1] - math.pi, 0)])
			angle = unwrap_angle(Bi[1] - math.pi, Ai[1]) - Ai[1]
			v_ = abs(angle / dt * Ai[0])
			if v_ > V: return Ai - (Vdt, 0)
			vr = math.sqrt(V * V - v_ * v_)
			return Ai + (vr * dt, angle)

		def fB(Bi, Ai):
			if Ai[0] == 0: return Bi
			angle = unwrap_angle(Ai[1] - Bi[1], 0)
			if angle < wdt: return Bi + (0, angle)
			return Bi + (0, wdt)

		def func(X):
			return [X[0] * math.cos(X[1]), X[0] * math.sin(X[1])]

		data = [[func(A), func(B)]]
		count = 1
		while count < 100000 and A[0] < R:
			t += dt
			A = fA(A, B)
			B = fB(B, A)
			data.append([func(A), func(B)])
			count += 1
		data = np.asarray(data)
		print(data.shape)
		print(dt * (count - 1))
		canvas = scene.SceneCanvas(keys = 'interactive')
		view = canvas.central_widget.add_view()
		view.set_camera('turntable', mode = 'perspective', up = 'z', distance = 2,
		                azimuth = 30., elevation = 65.)

		model = PCModel()
		circle1 = PCModel.circle((0, 0, 0), (0, 0, 1), KaisColor.plotColor("yellow") / 1.25, radius = R, density = 300)
		circle2 = PCModel.circle((0, 0, 0), (0, 0, 1), KaisColor.plotColor("crimson") / 1.1, radius = r, density = 300)
		model.add_model(circle1)
		model.add_model(circle2)
		H = np.linspace(-5, 5, count)
		modelA = PCModel(count)
		modelA.points[:, :2] = data[:, 0]
		modelA.points[:, 2] = H
		modelA.colors[:, :] = KaisColor.plotColorMap("cool", count)
		model.add_model(modelA)
		modelB = PCModel(count)
		modelB.points[:, :2] = data[:, 1]
		modelB.points[:, 2] = H
		modelB.colors[:, :] = KaisColor.plotColorMap("Wistia", count)
		model.add_model(modelB)

		model.save_to_las("/home/kai/Documents/GitHub/KaisMemory/PyhtonSample/math_game/chasing_circle.las")
		pass


	main()
	pass
