import cv2


def main():
	cap_L = cv2.VideoCapture(1)
	cap_R = cv2.VideoCapture(2)

	cv2.namedWindow("cam_L", cv2.WINDOW_AUTOSIZE)
	cv2.namedWindow("cam_R", cv2.WINDOW_AUTOSIZE)

	if cap_L.isOpened() and cap_R.isOpened():
		print(">> cameras start ..")
	else:
		print(">> err, can not open camera ..")
		exit(-1)

	# cap_L.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	# cap_L.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	# cap_R.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	# cap_R.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	# cap_L.set(cv2.CAP_PROP_FOCUS, 0)
	# cap_R.set(cv2.CAP_PROP_FOCUS, 0)

	is_running = True
	while is_running:
		ret_L, img_L = cap_L.read()
		ret_R, img_R = cap_L.read()

		if ret_L and ret_R:
			cv2.imshow("cam_L", img_L)
			cv2.imshow("cam_R", img_R)
			if cv2.waitKey(1) == 27:
				is_running = False
				print(">> exit ..")
		else: print(">> camera short circuit")
	print(">> process finished ..")


if __name__ == '__main__':
	main()
	pass
