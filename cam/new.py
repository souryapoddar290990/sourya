import cv2, os
import numpy as np
from PIL import Image

cascadePath = "/home/student/sourya/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.createLBPHFaceRecognizer()

train_image_list = ['cropped_a1.jpg','cropped_a2.jpg','cropped_a3.jpg','cropped_a4.jpg','cropped_a5.jpg','cropped_a6.jpg','cropped_a7.jpg','cropped_a8.jpg','cropped_a9.jpg','cropped_b1.jpg','cropped_b2.jpg','cropped_b3.jpg','cropped_b4.jpg','cropped_b5.jpg','cropped_b6.jpg','cropped_b7.jpg','cropped_b8.jpg','cropped_b9.jpg']
train_label_list = [1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2]
test_image_list = ['cropped_a10.jpg','cropped_b10.jpg']
test_label_list = [1,1]
images = []
labels = []
for index,item in enumerate(train_image_list):
    filename = 'cropped/'+item
    image_pil = Image.open(filename).convert('L')
    image = np.array(image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(image)
    for (x, y, w, h) in faces:
        images.append(image[y: y + h, x: x + w])
        labels.append(train_label_list[index])
        #cv2.imshow('',image[y: y + h, x: x + w])
        #cv2.waitKey(1000)

recognizer.train(images, np.array(labels))

for item in test_image_list:
    filename = 'cropped/'+item
    predict_image_pil = Image.open(filename).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        label_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        cv2.imshow('',predict_image[y: y + h, x: x + w])
        print label_predicted
        #cv2.waitKey(1000)




