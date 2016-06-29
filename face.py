import cv2,os,numpy,time,imutils,datetime,pprint

# ===================================================IMAGE=================================================================
# imagePath = 'face3.png'
# cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
# faceCascade = cv2.CascadeClassifier(cascPath)
# image = cv2.imread(imagePath)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# faces = faceCascade.detectMultiScale(gray,scaleFactor=1.8,minNeighbors=5,minSize=(50, 50))
# print "Found {0} faces!".format(len(faces))
# for (x, y, w, h) in faces:
#     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
# cv2.imshow("Faces found" ,image)
# cv2.waitKey(0)

# ========================================================VIDEO============================================================
# cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
# faceCascade = cv2.CascadeClassifier(cascPath)
# video_capture = cv2.VideoCapture(0)
# while True:
#     ret, frame = video_capture.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.imshow('Video', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# video_capture.release()
# cv2.destroyAllWindows()

# ====================================================MOTION===============================================================
def change(t0,t1,t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)
t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
while True:
    text = 0
    temp = cam.read()[1]
    frame = imutils.resize(temp, width=500)
    tmp = change(t0,t1,t2)
    count = 0
    for item in tmp:
        count += sum(item)
    # print count/480q
    if count > 1200*480:
        print "MOTION"
        text = 1
    else:
        print ""
    # cv2.imshow('Video',tmp)
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

# ====================================================PRESENCE=============================================================
# def change(t0,t1):
#     d = cv2.absdiff(t1, t0)
#     return d

# def send_push():
#     try:
#         title = "INTRUSION"
#         text = "movement detected"
#         from pushbullet import Pushbullet
#         API_KEY = 'o.nYHrQiyqBr2NTj59HaQFSSGsgoLDYQrv'
#         pb = Pushbullet(API_KEY)
#         push = pb.push_note(title,text)
#     except: pass

# def get_face(gray,frame,filename):
#     cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
#     faceCascade = cv2.CascadeClassifier(cascPath)
#     faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
#     cv2.imwrite(filename+'.png',frame)

# cam = cv2.VideoCapture(0)
# t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
# presence,absence = 0,0
# while True:
#     temp = cam.read()[1]
#     t1 = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
#     frame = imutils.resize(temp, width=500)
#     tmp = change(t0,t1)
#     count = 0
#     for item in tmp:
#         count += sum(item)
#     # print count/480
#     if count > 5000*480:
#         cv2.putText(frame, "Room Status: {}".format("Occupied"), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
#         presence += 1
#         absence = 0
#     else:
#         cv2.putText(frame, "Room Status: {}".format("Unoccupied"), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
#         absence += 1
#         if absence > 60: presence = 0
#     curr_time = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
#     filename = str(datetime.datetime.now().strftime("%d %B %I-%M-%S %p"))
#     cv2.putText(frame, curr_time,(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#     cv2.imshow("Security Feed", frame)
#     print presence,absence,count/480
#     # break
#     if presence > 60:
#         send_push()
#         presence = 0
#     if (presence-1)%2 == 0: get_face(t1,temp,filename)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cam.release()
# cv2.destroyAllWindows()