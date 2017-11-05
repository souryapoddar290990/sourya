# [78,55555,3,60]
# [73,7777,1,2,0,1]
# [73,8888,1,2,0,1]
# [73,5555,1,2,0,0]
# [73,6666,1,2,0,0]

# [53,123,1,4,
# [1,1,1,1,10],
# [1,2,1,1,10],
# [1,5,1,1,10],
# [2,1,1,5,6]]

# alfred_ids = [1,2,3,4]
# device_id = [0,2,4,5]

# [type,dev_id,alf_id,state,intensity]

# [53,TID,MODE_ID,Number_of_devices,[DEVICE_TYPE_1,Device_id,alfred_id,State,Intensity],[DEVICE_TYPE_2,Device_id,alfred_id,Model_id,Key_id],[DEVICE_TYPE_3,Security_State,0,0,0]]


# [153,12,1,4,[1,5,1,1,10],[1,5,2,1,10],[1,5,2,1,10],[1,5,3,1,10]]
# [153,13,2,4,[1,0,1,1,10],[1,2,1,1,10],[1,4,1,1,10],[1,5,1,1,10]]
# [153,22,3,4,[1,5,1,0,10],[1,5,2,0,10],[1,5,2,0,10],[1,5,3,0,10]]
# [153,33,4,4,[1,0,1,0,10],[1,2,1,0,10],[1,4,1,0,10],[1,5,1,0,10]]
# [153,12,1,5,[1,5,1,1,10],[1,5,2,1,10],[1,5,3,1,10],[1,5,4,1,10],[3,1,1,0,0]]
# [153,62,1,6,[1,5,1,1,10],[1,5,2,1,10],[1,5,3,1,10],[1,5,4,1,10],[2,5,1,1,1],[3,0,0,0,0]]
# [154,55,1]

        
# .aggregate([{'$match':{'user_id':user_id,'timestamp': {"$gte": start_time, "$lt": end_time}}},{'$group':{'_id':{'timestamp':'$timestamp','ssid':'$ssid',inside_home':'$inside_home','event_type':'$event_type'}}}])

# .aggregate([
# {$match: {created: {$gt: new Date(time)}}},
# {$group: {_id: null,count: {$sum: 1}}}
# ])

# [52, 5434, 1, 0, 3, [[1, 1, 1, 10, 0],[2, 1, 1, 10, 0],[3, 1, 1, 10, 0]]]
# node server_to_robin.js production 04-05-2016
      

# ObjectId("563b3b28595f6b5c6d887170")      

# 575e8ff1596448487e7790eb

# from iplotter import C3Plotter,ChartsJSPlotter,PlotlyPlotter
# from IPython.display import HTML

# def generate_donut_chart(counter,title):
# 	data = []
# 	for item in counter: data.append([item,counter[item]])
# 	chart = {
# 		'data': {
# 			'columns':data,
# 			'type' : 'donut',
# 		},
# 		'donut': {
# 			'title': title
# 		},
# 		'size': {
# 		  'width': 320,
# 		  'height': 320
# 		}
# 	}
# 	return chart

# chart_1 = generate_donut_chart({'36': 187, '37': 56, '35': 27},'plot_1')
# chart_2 = generate_donut_chart({'39': 1219, '37': 662, '38': 439, '36': 256, '35': 12},'plot_2')

# plotly_plotter = PlotlyPlotter()
# c3_plotter = C3Plotter()

# multiple_plot_html = plotly_plotter.head + c3_plotter.head
# multiple_plot_html += c3_plotter.render(data=chart_1, div_id="chart_1")
# multiple_plot_html += c3_plotter.render(data=chart_2, div_id="chart_2")
# HTML(c3_plotter.iframe.format(source=multiple_plot_html, w=600, h=900))
# with open("chart.html", 'w') as outfile:
#     outfile.write(multiple_plot_html)

# CONSIDER 1ST 10 FRAME AVERAGE AS BACKGROUD
# COMPUTE MASK FOR EACH FRAME AND SAVE
# CONVERT IMAGE INTO GRAYSCALE AND SAVE

# import cv2
# count = 0
# camera = cv2.VideoCapture(0)
# grabbed, frame = camera.read()
# first_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# first_frame = cv2.GaussianBlur(first_frame, (21, 21), 0)
# while True:
#     count += 1
#     grabbed, frame = camera.read()
#     frame_raw = frame.copy()
#     # cv2.imshow('original',frame_raw)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (21, 21), 0)
#     frameDelta = cv2.absdiff(first_frame, gray)
#     k = cv2.waitKey(1) & 0xff
#     # cv2.imshow('grayscale',gray)
#     cv2.imshow('diff',frameDelta)
#     # cv2.imwrite(str(count)+'.jpg',frame)
#     if k == 27:
#         break
# camera.release()
# cv2.destroyAllWindows()

import numpy as np
import cv2
# import time
# cap = cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorMOG2()
# while True:
#    ret, frame = cap.read()
#    fgmask = fgbg.apply(frame)
#    cv2.imshow('frame',fgmask)
#    k = cv2.waitKey(30) & 0xff
#    if k == 27:
#        break
# cap.release()
# cv2.destroyAllWindows()

def function5():
    # cam = cv2.VideoCapture(0)
    # cam = cv2.VideoCapture('output_video_clip_4.avi')
    cam = cv2.VideoCapture('http://camera.leaf.co.in/hls/568cc9bad5bda39f0a700b4c_57f771a2e9cb619114c7b5d7.m3u8')
    # cam = cv2.VideoCapture(0)
    bgsubtract = cv2.createBackgroundSubtractorMOG2()
    cv2.ocl.setUseOpenCL(False)
    count = 1000
    while True:
        count += 1
        # print count
        frame = cam.read()[1]
        frame_raw = frame.copy()
        # mask = bgsubtract.apply(frame)
        # ret,thresh1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # resized_gray = cv2.resize(gray, (240, 160))
        # resized_mask = cv2.resize(mask, (240, 160))
        cv2.imshow("webcam", frame_raw)
        # cv2.imshow("motion", mask)
        # cv2.imshow("GRAY",gray)
        # cv2.imwrite('gray_'+str(count)+'.png',resized_gray)
        # cv2.imwrite('mask_'+str(count)+'.png',resized_mask)
        # print 'train/gray_'+str(count)+'.png'
        # print 'train/mask_'+str(count)+'.png'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()    

function5()

