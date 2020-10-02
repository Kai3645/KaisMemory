import cv2
import numpy as np


def matching(img_base, img_add, count):
	detector = cv2.xfeatures2d.SIFT_create()
	# detector = cv2.xfeatures2d.SURF_create(500)
	kps1, des1 = detector.detectAndCompute(img_base, None)
	kps2, des2 = detector.detectAndCompute(img_add, None)

	FLANN_INDEX_KDTREE = 0  # 建立FLANN匹配器的参数
	indexParams = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	searchParams = dict(checks = 20)  # 指定递归次数
	matcher = cv2.FlannBasedMatcher(indexParams, searchParams)
	mts = matcher.knnMatch(des1, des2, k = 2)  # get matches

	good = []
	mtsMask = [[0, 0] for _ in range(len(mts))]
	# get good matches ratio test as per Lowe's paper
	for i, (m, n) in enumerate(mts):
		if m.distance < 0.6 * n.distance:
			mtsMask[i] = [1, 0]
			good.append(m)

	# step print out
	kws = dict(matchesMask = mtsMask, flags = 2)  # key words
	dst = cv2.drawMatchesKnn(img_base, kps1, img_add, kps2, mts, None, **kws)
	cv2.imwrite(main_path + "test_out/check_%02d_match.png" % count, dst)

	src_pts = np.array([kps1[m.queryIdx].pt for m in good])
	dst_pts = np.array([kps2[m.trainIdx].pt for m in good])
	move = src_pts - dst_pts
	offset = [np.sum([v[0] for v in move]) / len(move), np.sum([v[1] for v in move]) / len(move)]
	print(offset)


def reshape(src, mat):
	y_len, x_len = src.shape[:2]
	pos_src_ex = np.asarray([[0, 0, 1], [0, y_len, 1], [x_len, y_len, 1], [x_len, 0, 1]])
	pos_dst_ex = np.dot(pos_src_ex, mat.transpose())
	for p in pos_dst_ex: p[:] /= p[2]

	offset = np.asarray([min(p[0] for p in pos_dst_ex), min(p[1] for p in pos_dst_ex)])
	for p in pos_dst_ex: p[:2] -= offset
	size = (int(max(p[0] for p in pos_dst_ex)), int(max(p[1] for p in pos_dst_ex)))

	pos_src = np.float32(pos_src_ex[:, :2])
	pos_dst = np.float32(pos_dst_ex[:, :2])
	mat = cv2.getPerspectiveTransform(pos_src, pos_dst)

	mask_dst = np.full((y_len, x_len), 255, np.uint8)
	mask_dst = cv2.warpPerspective(mask_dst, mat, size, **kws_mask)
	dst = cv2.warpPerspective(src, mat, size, **kws_img)

	cv2.imwrite(main_path + "test_out/reshape_dst.png", dst)
	return dst, mask_dst, offset


def combine(base, mask_base, src, mask_src, offset):
	offset_global = np.asarray([min(offset[0], 0), min(offset[1], 0)]) * -1
	offset += offset_global

	shape_base = base.shape
	shape_src = src.shape
	shape_global = (
		max(int(offset_global[1] + shape_base[0]), int(offset[1] + shape_src[0])),
		max(int(offset_global[0] + shape_base[1]), int(offset[0] + shape_src[1])),
		max(shape_base[2], shape_src[2]),
	)
	size_global = (shape_global[1], shape_global[0])

	#  set image_base to right place
	base_big = cv2.copyMakeBorder(
		base, 0, shape_global[0] - shape_base[0], 0, shape_global[1] - shape_base[1],
		cv2.BORDER_REPLICATE
	)
	mat = np.float32([[1, 0, offset_global[0]], [0, 1, offset_global[1]]])
	base_big = cv2.warpAffine(base_big, mat, size_global, **kws_img)
	mask_base_big = np.zeros((shape_global[0], shape_global[1]), np.uint8)
	mask_base_big[:shape_base[0], :shape_base[1]] = mask_base
	mask_base_big = cv2.warpAffine(mask_base_big, mat, size_global, **kws_mask)
	cv2.imwrite(main_path + "test_out/combine_01_mask_base_big.png", mask_base_big)

	#  set image_src to right place
	src_big = cv2.copyMakeBorder(
		src, 0, shape_global[0] - shape_src[0], 0, shape_global[1] - shape_src[1],
		cv2.BORDER_REPLICATE
	)
	mat = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
	src_big = cv2.warpAffine(src_big, mat, size_global, **kws_img)
	mask_src_big = np.zeros((shape_global[0], shape_global[1]), np.uint8)
	mask_src_big[:shape_src[0], :shape_src[1]] = mask_src
	mask_src_big = cv2.warpAffine(mask_src_big, mat, size_global, **kws_mask)
	cv2.imwrite(main_path + "test_out/combine_02_mask_src_big.png", mask_src_big)

	#  set global masks
	mask_or = cv2.bitwise_or(mask_base_big, mask_src_big)
	mask_and = cv2.bitwise_and(mask_base_big, mask_src_big)
	mask_base_big = cv2.bitwise_xor(mask_base_big, mask_and)
	mask_src_big = cv2.bitwise_xor(mask_src_big, mask_and)

	# combine images todo make this better
	dst_and = cv2.addWeighted(base_big, 0.7, src_big, 0.3, 0)
	dst_and = cv2.bitwise_and(dst_and, dst_and, mask = mask_and)
	cv2.imwrite(main_path + "test_out/combine_03_dst_and.png", dst_and)

	base_big = cv2.bitwise_and(base_big, base_big, mask = mask_base_big)
	src_big = cv2.bitwise_and(src_big, src_big, mask = mask_src_big)
	dst = dst_and + base_big + src_big
	cv2.imwrite(main_path + "test_out/combine_04_dst.png", dst)

	return dst, mask_or


def main():
	count = 0
	img_base = cv2.imread(main_path + "img02.png")
	mask_base = np.full(img_base.shape[:2], 255, np.uint8)

	img_src_org = cv2.imread(main_path + "img03.png")
	matching(img_base, img_src_org, count)

	img_src, mask_src, offset = reshape(img_src_org, mat)
	img_base, mask_base = combine(img_base, mask_base, img_src, mask_src, offset)


if __name__ == '__main__':
	main_path = "/Users/kai/Library/Mobile Documents/com~apple~CloudDocs/Code/Python/imageProcess/img_daily/"
	kws_img = dict(borderMode = cv2.BORDER_REPLICATE, flags = cv2.INTER_CUBIC)
	kws_mask = dict(borderMode = cv2.BORDER_CONSTANT, flags = cv2.INTER_NEAREST)
	main()
