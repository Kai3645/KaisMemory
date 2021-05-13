import cv2

from Core.ComputerVision.camera_basic import chessboard_image

if __name__ == '__main__':
	BOARD_W = 7
	BOARD_H = 4
	board = chessboard_image((BOARD_W, BOARD_H), 1920)

	path = "/home/kai/PycharmProjects/pyCenter/diary_output/tmp/"
	cv2.imwrite(path + "chessboard.png", board)

