import cv2


def main():
    img_names = [main_path + "img01.png",
                 main_path + "img02.png",
                 main_path + "img03.png",
                 main_path + "img04.png"]
    imgs = []
    for img_name in img_names:
        imgs.append(cv2.imread(img_name))
    
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(imgs)
    cv2.imwrite("test_out/out.png", stitched)


if __name__ == '__main__':
    main_path = "img_daily/"
    
    main()
