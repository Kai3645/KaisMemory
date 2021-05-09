# import sys
# import time
#
# import cv2
# import numpy as np
#
#
# def main():
# 	folder = mkdir("/Users/kaismac/Downloads", "time_lapse")
#
# 	cap = cv2.VideoCapture(2)
# 	if not cap.isOpened():
# 		print(">> err, can not open camera ..")
# 		exit(-1)
#
# 	loop = 1
# 	FPS_SET = 1
# 	DT_SET = 1 / FPS_SET
#
# 	sys_delay = 60
# 	delay = 1000 / FPS_SET - sys_delay
#
# 	fps = FPS_SET
# 	text_max = 0
# 	ti = time.time()
# 	print(">> start ..")
# 	while True:
# 		print("\r" * text_max, end = "")
# 		ret, img = cap.read()
# 		if ret:
# 			img = cv2.GaussianBlur(img, (3, 3), 1.4)
#
# 			mask = np.zeros((160, 1100), np.uint8)
# 			info = time.strftime("%y.%m.%d %H:%M:%S", time.localtime())
# 			cv2.putText(mask, info, (23, 120), cv2.FONT_HERSHEY_DUPLEX, 3.5, 50, 15)
# 			cv2.putText(mask, info, (23, 120), cv2.FONT_HERSHEY_DUPLEX, 3.5, 240, 2)
# 			kernel = np.ones((5, 5), np.float32) / 25
# 			mask = cv2.filter2D(mask, -1, kernel)
#
# 			w, h, off1, off2 = 240, 44, 18, 13
# 			mask = cv2.resize(mask, (w, h), interpolation = cv2.INTER_CUBIC)
# 			mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
# 			sub_img = img[off2:h + off2, off1:w + off1].astype(int)
# 			ave = np.average(sub_img)
# 			if ave < 100:
# 				sub_img += mask
# 				sub_img[sub_img > 255] = 255
# 			elif ave < 160:
# 				valid = mask > 0
# 				sub_img[valid] = sub_img[valid] * 0.3 + mask[valid] * 1.2
# 				sub_img[sub_img > 255] = 255
# 			else:
# 				sub_img -= mask
# 				sub_img[sub_img < 0] = 0
# 			img[off2:h + off2, off1:w + off1, :] = sub_img.astype(np.uint8)
#
# 			img = cv2.resize(img, (1200, 675), interpolation = cv2.INTER_CUBIC)
# 			cv2.imwrite(folder + f"T{loop:05d}.jpg", img)
# 			sub_img = cv2.GaussianBlur(img, (3, 3), 1.22)
# 			sub_img = cv2.resize(sub_img, (800, 450), interpolation = cv2.INTER_CUBIC)
# 			cv2.imshow("camera", sub_img)
# 		else: print(">> camera short circuit")
# 		if cv2.waitKey(int(round(delay))) == 27: break
#
# 		t_ = ti
# 		ti = time.time()
# 		dt = ti - t_
# 		delay -= 20 * (1 / fps - DT_SET)
# 		fps = fps * 0.4 + 0.6 / dt
# 		info = f"{loop:06d}, fps = {fps:.3f}, delay = {delay:.0f}"
#
# 		info_len = len(info)
# 		if info_len < text_max: info += " " * (text_max - info_len)
# 		else: text_max = info_len
# 		print(info, end = "")
# 		loop += 1
# 	print()
# 	print(">> finished ..")
#
#
# if __name__ == '__main__':
# 	sys.path.append("/Users/kaismac/Documents/GitHub/ACRS_MMS/Python")
# 	from Core.Basic import mkdir
#
# 	main()
# 	pass
