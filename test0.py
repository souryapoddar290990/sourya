from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
count = 0
cam = cv2.VideoCapture('video4\output_video_clip_1.avi')
while True:
    count += 1
    image = cam.read()[1]
    #imagePath = "download.jpg"
    #image = cv2.imread(imagePath)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()
    pics = image.copy()
    (rects, weights) = hog.detectMultiScale(image, winStride=(8, 8), padding=(8, 8), scale=1.2)
    temp_count = 0
    # for (x, y, w, h) in rects:
        # temp_count += 1
        # cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv2.putText(orig,str(temp_count),(x,y+50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    # rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    # for (xA, yA, xB, yB) in pick:
        # cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
    #filename = imagePath[imagePath.rfind("/") + 1:]
    #print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))
    #cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", image)
    if cv2.waitKey(1) & 0xFF == ord("q"): break
    # print count,temp_count
cam.release()
cv2.destroyAllWindows()
