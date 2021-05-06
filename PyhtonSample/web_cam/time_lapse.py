import time

import cv2

from Core.Basic import mkdir


def main():
	folder = mkdir("/Users/kaismac/Downloads", "time_lapse")

	cap = cv2.VideoCapture(2)
	if not cap.isOpened():
		print(">> err, can not open camera ..")
		exit(-1)

	loop = 1
	FPS_SET = 1
	DT_SET = 1 / FPS_SET
	delay = 1000 / FPS_SET - 60

	t0 = ti = time.time()
	while True:
		ret, img = cap.read()
		if ret:
			img = cv2.GaussianBlur(img, (3, 3), 1.4)
			info = time.strftime("%y.%m.%d %H:%M:%S", time.localtime())
			cv2.putText(img, info, (20, 42), cv2.FONT_HERSHEY_DUPLEX, 0.9, [200, 200, 200], 6)
			cv2.putText(img, info, (20, 42), cv2.FONT_HERSHEY_DUPLEX, 0.9, [175, 175, 175], 3)
			cv2.putText(img, info, (20, 42), cv2.FONT_HERSHEY_DUPLEX, 0.9, [85, 85, 85], 2)
			cv2.putText(img, info, (20, 42), cv2.FONT_HERSHEY_DUPLEX, 0.9, [0, 0, 0], 1)
			img = cv2.resize(img, (1200, 675), interpolation = cv2.INTER_CUBIC)
			cv2.imwrite(folder + f"T{loop:05d}.jpg", img)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cv2.imshow(folder + f"cam", gray[::2, ::2])
		else:
			print(">> camera short circuit")
			break
		if cv2.waitKey(int(round(delay))) == 27: break

		t_ = ti
		ti = time.time()
		fps = loop / (ti - t0)
		delay -= 20 * (ti - t_ - DT_SET)
		print(f"{loop:06d}, fps = {fps:.3f}, delay = {delay:.0f}")
		loop += 1
	print(">> finished ..")


if __name__ == '__main__':
	main()
	pass
