import matplotlib.pyplot as plt
import cv2

filename = 0

def get_face(f1,f2,filename):
    cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    faces = faceCascade.detectMultiScale(f1,scaleFactor=1.1,minNeighbors=5,minSize=(20, 20))
    for (x, y, w, h) in faces:
        filename += 1
        cropped = f2.copy()[y:y+h,x:x+w]
        cv2.rectangle(f2, (x, y), (x+w, y+h), (255, 0, 0), 1)
        # cv2.imwrite(str(filename)+'.png',cropped)
        # print filename
    # cv2.imshow('face',f2)
    return filename

# camera = cv2.VideoCapture('C:/Users/DELL/Downloads/basic-motion-detection/videos/example_01.mp4')
# camera = cv2.VideoCapture(0)
# camera = cap = cv2.VideoCapture('output.avi')
camera = cv2.VideoCapture('http://leafcamera.ddns.net:9000/videostream.cgi?loginuse=admin&loginpas=admin')
# camera = cv2.VideoCapture('TheBigBangTheory.mkv')
t,l,w,h,motion_array,time_array,firstFrame,count,presence,absence,bufferframes,frame_rate,motion,video_num,video_new = 0,0,640,35,[],[],None,0,60,0,60,10,0,0,1
# plt.ion()
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter('output_'+str(video_num)+'.avi',fourcc, frame_rate, (int(camera.get(3)),int(camera.get(4))))
# print int(camera.get(3)),int(camera.get(4))

while True:
    try:
        count += 1
        grabbed, frame = camera.read()
        frame_raw = frame.copy()
        if count < bufferframes: continue
        text = "Unoccupied"
        if not grabbed: break

        # frame = imutils.resize(frame, width=500)
        # frame[t:t+h, l:l+w] = [0,0,255]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if firstFrame is None:
            firstFrame = gray
            continue
        frameDelta = cv2.absdiff(firstFrame, gray)
        frameDelta[t:t+h, l:l+w] = [0]
        thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
        if count%frame_rate == 0:
            plt.scatter(count,motion)
            plt.draw()
            motion = 0
        for c in cnts:
            if cv2.contourArea(c) < 1000: continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = (x+w/2,y+h/2)
            text = "Occupied"
            motion += 1

        if text == "Occupied":
            # print "MOTION"
            # filename = get_face(gray, frame_raw, filename)
            # if video_new == 1:
                # out = cv2.VideoWriter('output_'+str(video_num)+'.avi',fourcc, 20, (int(camera.get(3)),int(camera.get(4))))
                # video_new = 0
            # out.write(frame)
            presence -= 1
        if text == "Unoccupied":
            presence = 60
        motion_array.append(motion)
        time_array.append(count)
        # plt.scatter(count,motion)
        # plt.pause(0.0001)
        # plt.set_ydata(motion)
        # plt.draw()
        # cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),\(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)
        if cv2.waitKey(1) & 0xFF == ord("q"): break
        if presence <= 0:
            firstFrame = None
            presence = 60
            video_new = 1
            video_num += 1
            # out.release()
    # 	print time.time(),count,motion
    except Exception, e:
        print e
        break

camera.release()
cv2.destroyAllWindows()
print motion_array
print time_array
# fig = plt.figure()
# plt.plot(time_array,motion_array)
# plt.show()


