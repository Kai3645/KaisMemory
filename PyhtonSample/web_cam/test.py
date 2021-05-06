import cv2


def main():
	cap = cv2.VideoCapture(2)

	# cv2.namedWindow("cam", cv2.WINDOW_AUTOSIZE)
	# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	# cap.set(cv2.CAP_PROP_FOCUS, 0)

	if not cap.isOpened():
		print(">> err, can not open camera ..")
		exit(-1)

	is_running = True
	while is_running:
		ret, img = cap.read()

		if ret:
			cv2.imshow("cam", img[::5, ::5])
			if cv2.waitKey(1) == 27:
				is_running = False
				print(">> exit ..")
		else: print(">> camera short circuit")
	pass


if __name__ == '__main__':
	main()
	pass
