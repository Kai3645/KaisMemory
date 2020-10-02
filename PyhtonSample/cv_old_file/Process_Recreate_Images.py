import cv2
import numpy as np

from PointCloudModel import PCModel


def getCameraTransMat_rotOnly(MSCameraPosRot):
    matComplex = PCModel.transMat_B(MSCameraPosRot[3:6], MSCameraPosRot[0:3])
    matComplex = PCModel.matC2B * matComplex * PCModel.matB2C
    mat = matComplex[:3, :3]
    return mat


def reshape(src, mat):
    h, w = src.shape[:2]
    z0 = 1449.275362
    pos_src_ex = np.asarray([[-w / 2, -h / 2, z0], [-w / 2, h / 2, z0], [w / 2, h / 2, z0], [w / 2, -h / 2, z0]])
    pos_dst_ex = np.asarray(pos_src_ex * mat.transpose())
    for p in pos_dst_ex: p *= z0 / p[2]
    
    offset = np.asarray([min(p[0] for p in pos_dst_ex), min(p[1] for p in pos_dst_ex)])
    for p in pos_dst_ex: p[:2] -= offset
    size = (int(max(p[0] for p in pos_dst_ex)), int(max(p[1] for p in pos_dst_ex)))
    
    pos_src = np.float32([[0, 0], [0, h], [w, h], [w, 0]])
    pos_dst = np.float32(pos_dst_ex[:, :2])
    mat = cv2.getPerspectiveTransform(pos_src, pos_dst)
    
    mask_dst = np.full((h, w), 255, np.uint8)
    mask_dst = cv2.warpPerspective(mask_dst, mat, size, **kws_mask)
    dst = cv2.warpPerspective(src, mat, size, **kws_img)
    
    return dst, mask_dst, offset


def main():
    mat = getCameraTransMat_rotOnly((2.245, -0.05, -0.284, 0.25, -10.32, 29.90))
    img_src = cv2.imread(main_path + "01_539455.4289.png")
    img_dst, mask_dst, offset = reshape(img_src, mat)
    cv2.imwrite("out.png", img_dst)
    cv2.imwrite("msk.png", mask_dst)
    img_out = cv2.bitwise_and(img_dst, img_dst, mask = mask_dst)
    cv2.imwrite("out2.png", img_out)
    print(offset)


if __name__ == '__main__':
    main_path = "/Volumes/KaiのLaCie/Projects/source_Corrected_Sample_Images/image with normal size/"
    kws_img = dict(borderMode = cv2.BORDER_REPLICATE, flags = cv2.INTER_CUBIC)
    kws_mask = dict(borderMode = cv2.BORDER_CONSTANT, flags = cv2.INTER_NEAREST)
    main()
