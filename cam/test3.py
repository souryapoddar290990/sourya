import imutils,cv2,datetime

cam = cv2.VideoCapture('test.mp4')
t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
presence,absence = 0,0
while True:
    temp = cam.read()[1]
    t1 = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
    frame = imutils.resize(temp, width=500)
    count = int(cv2.norm(t0,t1,cv2.NORM_L1))
    print count/360
    if count > 5000*360:
        cv2.putText(frame, "Room Status: {}".format("Occupied"), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        presence += 1
        absence = 0
    else:
        cv2.putText(frame, "Room Status: {}".format("Unoccupied"), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        absence += 1
        if absence > 60: presence = 0
    curr_time = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
    filename = str(datetime.datetime.now().strftime("%d %B %I-%M-%S %p"))
    cv2.putText(frame, curr_time,(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)
    print presence,absence,count/480
    # break
    if presence > 60:
        # send_push()
        presence = 0
    #if (presence-1)%5 == 0: get_face(t1,temp,filename)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
