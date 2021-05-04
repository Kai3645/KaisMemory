import cv2

from Core.Basic import err_exit


def main():
	capture = cv2.VideoCapture(2)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	capture.set(cv2.CAP_PROP_FOCUS, 0)
	# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	print(capture.isOpened())
	if not capture.isOpened(): err_exit("err, video not open ..")
	for i in range(10):
		ret, img = capture.read()
		cv2.imshow("", img)
		cv2.waitKey()
	pass


if __name__ == '__main__':
	main()
	pass
