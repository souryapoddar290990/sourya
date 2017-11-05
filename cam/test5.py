import cv2
import numpy as np
 
cam = cv2.VideoCapture('test.mp4')
frame = cam.read()[1]
avg = np.float32(frame)
 
while True:
    frame = cam.read()[1]
    cv2.accumulateWeighted(frame,avg,0.1)
    res = cv2.convertScaleAbs(avg)
    #cv2.imshow('img',frame)
    cv2.imshow('avg2',res)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
 
cv2.destroyAllWindows()
cam.release()
