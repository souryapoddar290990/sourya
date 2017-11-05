# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# cv2.destroyAllWindows()
# capture = cv2.VideoCapture('test1.mp4')
# numframes = int(capture.get(7))
# count = 0
# bgs = cv2.createBackgroundSubtractorMOG2()

# plt.figure()
# plt.hold(True)
# plt.axis([0,480,360,0])

# measuredTrack = np.zeros((numframes,2))-1
# while count<numframes:
#     count += 1
#     img2 = capture.read()[1]
#     cv2.imshow("Video",img2)
#     foremat=bgs.apply(img2)
#     ret,thresh = cv2.threshold(foremat,127,255,0)
#     contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]
#     if len(contours) > 0:
#         m = np.mean(contours[0],axis=0)
#         measuredTrack[count-1,:]=m[0]
#         plt.plot(m[0,0],m[0,1],'ob')
#     cv2.imshow('Foreground',foremat)
#     if cv2.waitKey(1) & 0xFF == ord('q'): break
# capture.release()
# cv2.destroyAllWindows()
# plt.show()

