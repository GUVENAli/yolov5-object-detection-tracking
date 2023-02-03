import cv2
import numpy as np
import os
import json

cap = cv2.VideoCapture("./challenge/images/train/train.mp4")
with open("./challenge/annotations/instances_train.json") as f:
    data = json.load(f)
anno1 = data["annotations"]
arr = np.arange(7200)
i = 0
anno_ind = 0
classes = ["bolt", "nut"]
while 1:
    g, f = cap.read()
    if not g or cv2.waitKey(5) == 27:
        break
    img_id = anno1[anno_ind]["image_id"]
    bbox = anno1[anno_ind]["bbox"]
    cat = anno1[anno_ind]["category_id"]
    while i == img_id:
        f = cv2.rectangle(f, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (0, 0, 255), 2)
        f = cv2.putText(f, classes[cat-1], (int(bbox[0]), int(bbox[1] + bbox[3])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        anno_ind += 1
        img_id = anno1[anno_ind]["image_id"]
        bbox = anno1[anno_ind]["bbox"]
        cat = anno1[anno_ind]["category_id"]

    cv2.imshow("frame", f)
    cv2.waitKey(20)
    i += 1
cap.release()
cv2.destroyWindow()