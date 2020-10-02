import cv2
import numpy as np


def main():
    img = cv2.imread("img_00.png")
    
    # calc by hand
    pos_src = np.float32([[0, 0], [0, 3024], [4032, 3024], [4032, 0]])
    pos_dst = np.float32([[0, 0], [133.093, 3046.817], [4049.504, 3046.817], [4186.597, 0]])
    
    mat = cv2.getPerspectiveTransform(pos_src, pos_dst)
    
    dst = cv2.warpPerspective(img, mat, (4186, 3046), flags = cv2.INTER_CUBIC)
    cv2.imwrite("/Users/kai/ProjectCenter/OpencvProject/test_out/out_check.png", dst)
    # dst = dst[20:3020, 135:4047]
    cv2.imwrite("img_00_shaped.png", dst)


if __name__ == '__main__':
    main_path = "imgs/"
    
    main()
