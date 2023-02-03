import json
import os
from argparse import ArgumentParser
from tqdm import tqdm
import glob

def find_anns(anno, id):
    img_w = 640
    img_h = 640
    out = []
    for i in anno:
        img_id = i["image_id"]
        bbox = i["bbox"]
        cat = i["category_id"]
        if img_id == id:
            x = bbox[0]
            y = bbox[1]
            w = bbox[2]
            h = bbox[3]

            x_center = (x + (x + w)) / 2
            y_center = (y + (y + h)) / 2

            x_center = x_center / img_w
            y_center = y_center / img_h
            w = w / img_w
            h = h / img_h

            x_center = format(x_center, '.6f')
            y_center = format(y_center, '.6f')
            w = format(w, '.6f')
            h = format(h, '.6f')
            cat = cat - 1
            out.append([cat, x_center, y_center, w, h])
    return out

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, default="val", help="choose the mode of created dataset if train, val, or test")
    parser.add_argument("-p", "--path", type=str, default="./challenge/annotations/instances_val.json",
                        help="path of the annotations of chosen dataset mode as json")
    parser.add_argument("-s", "--save", type=str, default="./yolov5/datasets/labels/val/",
                        help="path of images created to save as txt yolo format")
    parser.add_argument("-i", "--image", type=str, default="./yolov5/datasets/images/val/",
                        help="path of images created to save as txt yolo format")

    args = vars(parser.parse_args())
    mode = args["mode"]
    path = args["path"]
    save_path = args["save"]
    image_path = args["image"]

    imgs = glob.glob(image_path + "*.jpg")
    imgs_num = sorted([int(i.split("_")[-1][0:-4]) for i in imgs])

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(path, "r") as f:
        data = json.load(f)
    anno = data["annotations"]

    anno_ind = 0
    classes = ["bolt", "nut"]
    change = True
    temp = -1

    for image in tqdm(imgs_num):
        if image == temp:
            name = f"im_r_{image}.txt"
        else:
            name = f"im_{image}.txt"
        out = find_anns(anno, image)
        if out == []:
            f = open(save_path + name, "w")
        else:
            f = open(save_path + name, "w")
            for v in range(len(out)):
                if v != len(out) - 1:
                    for w in range(len(out[v])):
                        if w != len(out[v]) - 1:
                            f.write(str(out[v][w]) + " ")
                        else:
                            f.write(str(out[v][w]) + "\n")
                else:
                    for w in range(len(out[v])):
                        if w != len(out[v]) - 1:
                            f.write(str(out[v][w]) + " ")
                        else:
                            f.write(str(out[v][w]))
        anno_ind += 1
        if anno_ind > 0:
            temp = image
        f.close()



