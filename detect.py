# from collections import deque
# import numpy as np
# import argparse
# import imutils
# import cv2

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=32, help="max buffer size")
# args = vars(ap.parse_args())

# Lower = (50, 0, 50)
# Upper = (80, 255, 80)

# pts = deque(maxlen=args["buffer"])
# counter = 0
# (dX, dY) = (0, 0)
# direction = ""

# camera = cv2.VideoCapture(0)
# while True:
# 	(grabbed, frame) = camera.read()
# 	if args.get("video") and not grabbed: break

# 	frame = imutils.resize(frame, width=600)
# 	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
# 	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 	mask = cv2.inRange(hsv, Lower, Upper)
# 	mask = cv2.erode(mask, None, iterations=2)
# 	mask = cv2.dilate(mask, None, iterations=2)

# 	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
# 	center = None

# 	if len(cnts) > 0:
# 		c = max(cnts, key=cv2.contourArea)
# 		((x, y), radius) = cv2.minEnclosingCircle(c)
# 		M = cv2.moments(c)
# 		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
# 		if radius > 20:
# 			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
# 			cv2.circle(frame, center, 5, (0, 0, 255), -1)
# 			pts.appendleft(center)

# 	for i in np.arange(1, len(pts)):
# 		if pts[i - 1] is None or pts[i] is None: continue
# 		if counter >= 10 and i == 1 and pts[-10] is not None:
# 			dX = pts[-10][0] - pts[i][0]
# 			dY = pts[-10][1] - pts[i][1]
# 			(dirX, dirY) = ("", "")

# 			if np.abs(dX) > 20: dirX = "East" if np.sign(dX) == 1 else "West"
# 			if np.abs(dY) > 20: dirY = "North" if np.sign(dY) == 1 else "South"
# 			if dirX != "" and dirY != "": direction = "{}-{}".format(dirY, dirX)
# 			else: direction = dirX if dirX != "" else dirY

# 		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
# 		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

# 	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 3)
# 	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

# 	cv2.imshow("Frame", frame)
# 	key = cv2.waitKey(1) & 0xFF
# 	counter += 1
# 	if key == ord("q"): break

# camera.release()
# cv2.destroyAllWindows()

############################################################### SKIN ########################################################
# import imutils,cv2
# import numpy as np

# lower = np.array([0, 0, 80], dtype = "uint8")
# upper = np.array([20, 255, 255], dtype = "uint8")
# camera = cv2.VideoCapture(0)

# while True:
# 	(grabbed, frame) = camera.read()

# 	if not grabbed: break
# 	frame = imutils.resize(frame, width = 400)
# 	converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# 	skinMask = cv2.inRange(converted, lower, upper)

# 	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
# 	skinMask = cv2.erode(skinMask, kernel, iterations = 2)
# 	skinMask = cv2.dilate(skinMask, kernel, iterations = 2)

# 	skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
# 	skin = cv2.bitwise_and(frame, frame, mask = skinMask)
# 	cv2.imshow("images", np.hstack([frame, skin]))
# 	if cv2.waitKey(1) & 0xFF == ord("q"):
# 		break

# camera.release()
# cv2.destroyAllWindows()

########################################################### PHOTOBOOTH ######################################################
# from PIL import Image
# from PIL import ImageTk
# import Tkinter as tki
# import threading,datetime,time,imutils,cv2,os
# from imutils.video import VideoStream

# class PhotoBoothApp:

# 	def __init__(self, vs, outputPath):
# 		# store the video stream object and output path, then initialize
# 		# the most recently read frame, thread for reading frames, and
# 		# the thread stop event
# 		self.vs = vs
# 		self.outputPath = outputPath
# 		self.frame = None
# 		self.thread = None
# 		self.stopEvent = None

# 		# initialize the root window and image panel
# 		self.root = tki.Tk()
# 		self.panel = None

# 		# create a button, that when pressed, will take the current
# 		# frame and save it to file
# 		btn = tki.Button(self.root, text="Snapshot!",
# 			command=self.takeSnapshot)
# 		btn.pack(side="bottom", fill="both", expand="yes", padx=10,
# 			pady=10)

# 		# start a thread that constantly pools the video sensor for
# 		# the most recently read frame
# 		self.stopEvent = threading.Event()
# 		self.thread = threading.Thread(target=self.videoLoop, args=())
# 		self.thread.start()

# 		# set a callback to handle when the window is closed
# 		self.root.wm_title("PyImageSearch PhotoBooth")
# 		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

# 	def videoLoop(self):
# 		# DISCLAIMER:
# 		# I'm not a GUI developer, nor do I even pretend to be. This
# 		# try/except statement is a pretty ugly hack to get around
# 		# a RunTime error that Tkinter throws due to threading
# 		try:
# 			# keep looping over frames until we are instructed to stop
# 			while not self.stopEvent.is_set():
# 				# grab the frame from the video stream and resize it to
# 				# have a maximum width of 300 pixels
# 				self.frame = self.vs.read()
# 				self.frame = imutils.resize(self.frame, width=300)
		
# 				# OpenCV represents images in BGR order; however PIL
# 				# represents images in RGB order, so we need to swap
# 				# the channels, then convert to PIL and ImageTk format
# 				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
# 				image = Image.fromarray(image)
# 				image = ImageTk.PhotoImage(image)
		
# 				# if the panel is not None, we need to initialize it
# 				if self.panel is None:
# 					self.panel = tki.Label(image=image)
# 					self.panel.image = image
# 					self.panel.pack(side="left", padx=10, pady=10)
		
# 				# otherwise, simply update the panel
# 				else:
# 					self.panel.configure(image=image)
# 					self.panel.image = image

# 		except RuntimeError, e:
# 			print("[INFO] caught a RuntimeError")

# 	def takeSnapshot(self):
# 		# grab the current timestamp and use it to construct the
# 		# output path
# 		ts = datetime.datetime.now()
# 		filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
# 		p = os.path.sep.join((self.outputPath, filename))

# 		# save the file
# 		cv2.imwrite(p, self.frame.copy())
# 		print("[INFO] saved {}".format(filename))

# 	def onClose(self):
# 		# set the stop event, cleanup the camera, and allow the rest of
# 		# the quit process to continue
# 		print("[INFO] closing...")
# 		self.stopEvent.set()
# 		self.vs.stop()
# 		self.root.quit()

# print("[INFO] warming up camera...")
# vs = VideoStream(0).start()
# time.sleep(2.0)

# pba = PhotoBoothApp(vs, '')
# pba.root.mainloop()

####################################################### GESTURE #############################################################

# import cv2
# import numpy as np
# import math
# cap = cv2.VideoCapture(0)
# while(cap.isOpened()):
#     ret, img = cap.read()
#     cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
#     crop_img = img[100:300, 100:300]
#     grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
#     value = (35, 35)
#     blurred = cv2.GaussianBlur(grey, value, 0)
#     _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#     cv2.imshow('Thresholded', thresh1)

#     # uncomment the lines below(17-18) if using OpenCV 3+ and remove lines 21-22
#     image, contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#     # works only for OpenCV 2.4.x
#     # contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#     max_area = -1
#     for i in range(len(contours)):
#         cnt=contours[i]
#         area = cv2.contourArea(cnt)
#         if(area>max_area):
#             max_area=area
#             ci=i
#     cnt=contours[ci]
#     x,y,w,h = cv2.boundingRect(cnt)
#     cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
#     hull = cv2.convexHull(cnt)
#     drawing = np.zeros(crop_img.shape,np.uint8)
#     cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
#     cv2.drawContours(drawing,[hull],0,(0,0,255),0)
#     hull = cv2.convexHull(cnt,returnPoints = False)
#     defects = cv2.convexityDefects(cnt,hull)
#     count_defects = 0
#     cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
#     for i in range(defects.shape[0]):
#         s,e,f,d = defects[i,0]
#         start = tuple(cnt[s][0])
#         end = tuple(cnt[e][0])
#         far = tuple(cnt[f][0])
#         a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
#         b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
#         c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
#         angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
#         if angle <= 90:
#             count_defects += 1
#             cv2.circle(crop_img,far,1,[0,0,255],-1)
#         #dist = cv2.pointPolygonTest(cnt,far,True)
#         cv2.line(crop_img,start,end,[0,255,0],2)
#         #cv2.circle(crop_img,far,5,[0,0,255],-1)
#     if count_defects == 1:
#         cv2.putText(img,"I am Vipul", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
#     elif count_defects == 2:
#         str = "This is a basic hand gesture recognizer"
#         cv2.putText(img, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
#     elif count_defects == 3:
#         cv2.putText(img,"This is 4 :P", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
#     elif count_defects == 4:
#         cv2.putText(img,"Hi!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
#     else:
#         cv2.putText(img,"Hello World!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
#     #cv2.imshow('drawing', drawing)
#     #cv2.imshow('end', crop_img)
#     cv2.imshow('Gesture', img)
#     all_img = np.hstack((drawing, crop_img))
#     cv2.imshow('Contours', all_img)
#     k = cv2.waitKey(10)
#     if k == 27:
#         break

######################################################### DRONE #############################################################

# import numpy as np
# import cv2

# def run_main():
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()

#     c,r,w,h = 200,250,70,70
#     track_window = (c,r,w,h)

#     # Create mask and normalized histogram
#     roi = frame[r:r+h, c:c+w]
#     hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv_roi, np.array((0., 30.,32.)), np.array((180.,255.,255.)))
#     roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
#     cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
#     term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1)
    
#     while True:
#         ret, frame = cap.read()
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180], 1)
#         ret, track_window = cv2.meanShift(dst, track_window, term_crit)
#         x,y,w,h = track_window
#         # print track_window
#         cv2.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
#         cv2.putText(frame, 'Tracked', (x-25,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
#         cv2.imshow('Tracking', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'): break

#     cap.release()
#     cv2.destroyAllWindows()

# run_main()