import numpy as np
import os
import cv2
from argparse import ArgumentParser
from tqdm import tqdm

# train_path = "./challenge/images/train/train.mp4"
# val_path = "./challenge/images/val/val.mp4"
# test_path = "./challenge/images/test/test.mp4"

def robustness(num, f, count, save_path):
    if num == 3:
        f = cv2.convertScaleAbs(f, alpha=float(np.random.rand(1) + 0.01), beta=0.8)
        cv2.imwrite(save_path + f"im_r_{count}.jpg", f)
        return f
    elif num == 5:
        f = cv2.blur(f,(9,9))
        cv2.imwrite(save_path + f"im_r_{count}.jpg", f)
        return f
    else:
        return f

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, default="test", help="choose the mode of created dataset if train, val, or test")
    parser.add_argument("-p", "--path", type=str, default="./challenge/images/test/test.mp4",
                        help="path of the video of chosen dataset mode")
    parser.add_argument("-s", "--save", type=str, default="./yolov5/datasets/images/test/",
                        help="path of images created to save")

    args = vars(parser.parse_args())
    mode = args["mode"]
    path = args["path"]
    save_path = args["save"]

    cap = cv2.VideoCapture(path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    count = 0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in tqdm(range(total)):
        g, f = cap.read()
        if not g:
            break
        # f = cv2.convertScaleAbs(f, alpha=float(np.random.rand(1) + 0.01), beta=0.1)
        # f = cv2.blur(f,(9,9))
        # cv2.imshow("a", f)
        f = cv2.resize(f, (224, 224))
        cv2.imwrite(save_path + f"im_{count}.jpg", f)
        num = np.random.randint(10)
        f = robustness(num, f, count, save_path)
        cv2.waitKey(10)
        count += 1
    cap.release()


