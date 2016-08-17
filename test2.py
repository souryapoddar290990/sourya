import cv2,imutils,datetime

def change(t0,t1,t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture('test.mp4')
t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
while True:
    text = 0
    temp = cam.read()[1]
    frame = imutils.resize(temp, width=500)
    tmp = change(t0,t1,t2)
    count = int(cv2.norm(tmp, cv2.NORM_L1))
    # print count/480
    if count > 600*360:
        print "MOTION"
        text = 1
    else:
        print ""
    cv2.imshow('Video',tmp)
    t0 = t1
    t1 = t2
    t2 = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
    if text == 0: cv2.putText(frame, "Room Status: {}".format("No Motion"), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if text == 1: cv2.putText(frame, "Room Status: {}".format("Motion"), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # cv2.imshow("Security Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
