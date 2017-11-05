import sys, os, cv2
sys.path.append("../..")
from facerec.feature import Fisherfaces, SpatialHistogram, Identity
from facerec.distance import EuclideanDistance, ChiSquareDistance
from facerec.classifier import NearestNeighbor
from facerec.model import PredictableModel
from facerec.validation import KFoldCrossValidation
from facerec.visual import subplot
from facerec.util import minmax_normalize
from facerec.serialization import save_model, load_model
import numpy as np
try: from PIL import Image
except ImportError: import Image
import matplotlib.cm as cm
import logging
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from facerec.lbp import LPQ, ExtendedLBP

path = "../../../../cropped/train"
size = (32,32)
threshold = 10.0

def read_images(path, sz=None):
    c = 0
    X,y = [], []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = Image.open(os.path.join(subject_path, filename))
                    im = im.convert("L")
                    if (sz is not None):
                        im = im.resize(sz, Image.ANTIALIAS)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(int(subdirname.replace("person",""))-1)
                    #y.append(c)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,y]

def validation(X,y,model):
    E = []
    for i in xrange(min(model.feature.eigenvectors.shape[1], 16)):
        e = model.feature.eigenvectors[:,i].reshape(X[0].shape)
        E.append(minmax_normalize(e,0,255, dtype=np.uint8))
    cv = KFoldCrossValidation(model, k=10)
    cv.validate(X, y)
    cv.print_results()

def prediction(model,query,threshold,size):
    im = Image.open(query)
    im = im.convert('L')
    im = im.resize(size, Image.ANTIALIAS)
    query = np.asarray(im, dtype=np.uint8)
    prediction = model.predict(query)
    predicted_label = prediction[0]
    classifier_output = prediction[1]
    distance = classifier_output['distances'][0]
    print distance,predicted_label+1
    #if distance > threshold: print "Unknown Person!"
    #else: print "Person is known with label %i" % (predicted_label+1) 

def face(query,my_model):
    temp = 'temp.jpg'
    frame = cv2.imread(query)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascPath = "/home/student/sourya/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(20, 20))
    for (x, y, w, h) in faces:
        cropped = frame.copy()[y:y+h,x:x+w]
        cv2.imwrite(temp,cropped)
        prediction(my_model,temp,10.0,size)
        
def get_face(faceCascade,gray,frame,filename=None):
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(20, 20))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
    #cv2.imshow('face',frame)
    #cv2.imwrite(filename+'.png',frame)

def main(path,size,threshold):
    cascPath = '/home/student/sourya/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    #[X,y] = read_images(path,size)
    #print y
    #handler = logging.StreamHandler(sys.stdout)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #handler.setFormatter(formatter)
    #logger = logging.getLogger("facerec")
    #logger.addHandler(handler)
    #logger.setLevel(logging.DEBUG)
    #feature = Fisherfaces()
    #classifier = NearestNeighbor(dist_metric=EuclideanDistance(), k=5)
    #my_model = PredictableModel(feature=feature, classifier=classifier)
    #my_model.compute(X,y)
    #save_model('model.pkl', my_model)
    #model = load_model('model.pkl')
    #validation(X, y, my_model)
    #query_image = "../../../../cropped/test/person1/cropped_a6.jpg"
    #prediction(my_model,query_image,10.0,size)
    #query_image = "../../../../cropped/test/person2/cropped_b6.jpg"
    #prediction(my_model,query_image,10.0,size)
    #query_image = "../../../../cropped/test/person3/cropped_c6.jpg"
    #prediction(my_model,query_image,10.0,size)
    #query_image = "../../../../cropped/test/person4/cropped_d6.jpg"
    #prediction(my_model,query_image,10.0,size)
    #query_image = "../../../../cropped/test/cropped_images5.jpg"
    #prediction(my_model,query_image,10.0,size)
    #face(query_image,my_model) 
    cam = cv2.VideoCapture('../../../../TheBigBangTheory.mkv')
    while True:
        temp = cam.read()[1]
        gray = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        cv2.imshow('face',temp)
        get_face(faceCascade,gray,temp)

main(path,size,threshold)
