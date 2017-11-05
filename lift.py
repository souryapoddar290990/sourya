import numpy as np
import cv2,os,imutils,requests,pprint,json
from PIL import Image
from subprocess import call,check_output

def split_image_new(image_path):
    filenames = []
    parts = 3
    ext = image_path.split(".")[-1]
    im = Image.open(image_path)
    width,height = im.size
    step_horizontal = width / parts
    step_vertical   = height / parts
    for i in range(parts):
        start1 = i*step_horizontal
        end1   = start1 + step_horizontal
        box = (start1, 0, end1, height)
        new = im.crop(box)
        filename = "sm1_"+str(i)+'.jpg'
        new.save(filename)
        filenames.append(filename)
    # for j in range(parts):
    #     start2 = j*step_vertical
    #     end2   = start2 + step_vertical
    #     box = (0, start2, width,end2)
    #     new = im.crop(box)
    #     filename = "sm2_"+str(j)+'.jpg'
    #     new.save(filename)
    #     filenames.append(filename)            
    return filenames

def take_frames(video_path):
    filenames = []
    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture(0)
    count = 10000
    while(1):
        count += 1
        # print count
        ret, frame = cap.read()
        if ret == False:
            # print filenames
            return
        if count%250 == 0:
            filename = "lift_"+str(count)+".jpg"
            cv2.imwrite(filename,frame)
            filenames.append(filename)
            print test_sm(filename)
        # cv2.imshow('',frame)
        cv2.waitKey(40)

def test_sm(filename):
	print filename
	results = []
	filenames = split_image_new(filename)
	for filename in filenames:
		command = 'python /usr/local/lib/python2.7/dist-packages/tensorflow/models/image/imagenet/classify_image.py --image_file '+filename
		temp = check_output(command, shell=True)
		result = json.loads(temp)
		for item in result:
			# print item['name']
			if item['name'] == 'ski mask':
				# print float(item['score'])
				if float(item['score'])*1000 > 2: results.append(1)
				else: results.append(0)
	# print result
	if sum(results) > 0: return 1
	else: return 0

# video_path = "../Documents/VM/anomaly_detection_code/code/demo_room.avi"
video_path = 'lift.mp4'
take_frames(video_path)

# LIFT
# filenames_lift = ['lift_10250.jpg','lift_10500.jpg','lift_10750.jpg','lift_11000.jpg','lift_11250.jpg','lift_11500.jpg','lift_11750.jpg','lift_12000.jpg','lift_12250.jpg','lift_12500.jpg','lift_12750.jpg','lift_13000.jpg','lift_13250.jpg','lift_13500.jpg','lift_13750.jpg','lift_14000.jpg','lift_14250.jpg','lift_14500.jpg','lift_14750.jpg','lift_15000.jpg']
# result_lift =      [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]
# predicted_lift_2 = [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1]
# predicted_lift_3 = [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]
# predicted_lift_4 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]

# STORE
# filenames_store = ['store_10250.jpg','store_10500.jpg','store_10750.jpg','store_11000.jpg','store_11250.jpg','store_11500.jpg','store_11750.jpg','store_12000.jpg','store_12250.jpg','store_12500.jpg','store_12750.jpg','store_13000.jpg','store_13250.jpg','store_13500.jpg','store_13750.jpg','store_14000.jpg','store_14250.jpg','store_14500.jpg','store_14750.jpg','store_15000.jpg','store_15250.jpg','store_15500.jpg','store_15750.jpg','store_16000.jpg','store_16250.jpg','store_16500.jpg','store_16750.jpg']
# result_store =      [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1]
# predicted_store_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# predicted_store_3 = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# predicted_store_4 = [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# ATM
# filenames_atm = ['atm_10250.jpg','atm_10500.jpg','atm_10750.jpg','atm_11000.jpg','atm_11250.jpg','atm_11500.jpg','atm_11750.jpg','atm_12000.jpg','atm_12250.jpg','atm_12500.jpg','atm_12750.jpg','atm_13000.jpg','atm_13250.jpg','atm_13500.jpg','atm_13750.jpg','atm_14000.jpg','atm_14250.jpg','atm_14500.jpg','atm_14750.jpg','atm_15000.jpg','atm_15250.jpg','atm_15500.jpg']
# result_atm =      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# predicted_atm_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# predicted_atm_3 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# predicted_atm_4 = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1]

# MASK
# filenames_mask = ['mask_10250.jpg','mask_10500.jpg','mask_10750.jpg','mask_11000.jpg','mask_11250.jpg','mask_11500.jpg','mask_11750.jpg','mask_12000.jpg','mask_12250.jpg']
# result_mask =      [0, 0, 1, 0, 0, 1, 0, 1, 0]
# predicted_mask_2 = [1, 1, 1, 1, 0, 1, 1, 1, 1]
# predicted_mask_3 = [1, 1, 1, 1, 0, 1, 1, 0, 1]
# predicted_mask_4 = [0, 1, 1, 1, 1, 1, 1, 0, 0]

# predicted = []
# for item in filenames_mask:
# 	predicted.append(test_sm(item))
# print predicted

# diff = [result_lift[i] - predicted_lift_3[i] for i in range(len(result_lift))]
# print diff
# for index,item in enumerate(diff):
	# if item == -1:
		# paia+1 filenames_lift[index]
		# test_sm(filenames[index])
