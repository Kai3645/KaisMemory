import cv2

if __name__ == '__main__':
	folder = "/Users/kaismac/.virtualenvs/pyCenter/output/"

	detector = cv2.xfeatures2d.SURF_create()
	src = cv2.imread("/Users/kaismac/Library/Mobile Documents/com~apple~CloudDocs/Code/0_system/test.jpg")
	kps = detector.detect(src)
	dst = cv2.drawKeypoints(src, kps, src, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imwrite(folder + "out_SURF.jpg", dst)

	detector = cv2.SIFT_create()
	src = cv2.imread("/Users/kaismac/Library/Mobile Documents/com~apple~CloudDocs/Code/0_system/test.jpg")
	kps = detector.detect(src)
	dst = cv2.drawKeypoints(src, kps, src, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imwrite(folder + "out_SIFT.jpg", dst)
