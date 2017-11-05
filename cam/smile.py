import matplotlib
from pylab import *
from sklearn import datasets
from IPython.html import widgets
from IPython.display import *
import json
import cv2
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem
from sklearn import metrics
from matplotlib.patches import Rectangle
from scipy.ndimage import zoom
import matplotlib.pyplot as plt

faces = datasets.fetch_olivetti_faces()
# print faces.keys()
# for i in range(10):
#     face = faces.images[i]
#     plt.subplot(1, 10, i + 1)
#     plt.imshow(face.reshape((64, 64)), cmap='gray')
#     axis('off')
# plt.show()

class Trainer:

    def __init__(self):
        self.results = {}
        self.imgs = faces.images
        self.index = 0
        
    def increment_face(self):
        if self.index + 1 >= len(self.imgs):
            return self.index
        else:
            while str(self.index) in self.results:
                print self.index
                self.index += 1
            return self.index
    
    def record_result(self, smile=True):
        self.results[str(self.index)] = smile

trainer = Trainer()
button_smile = widgets.Button(description='smile')
button_no_smile = widgets.Button(description='sad face')

def display_face(face):
    clear_output()
    plt.imshow(face, cmap='gray')
    plt.show()
    axis('off')

def update_smile(b):
    trainer.record_result(smile=True)
    trainer.increment_face()
    display_face(trainer.imgs[trainer.index])

def update_no_smile(b):
    trainer.record_result(smile=False)
    trainer.increment_face()
    display_face(trainer.imgs[trainer.index])

def plt_figure(param,text):
    face_indices = [int(i) for i in results if results[i] == param]
    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)
    for i in range(len(face_indices)):
        p = fig.add_subplot(20, 20, i + 1)
        p.imshow(faces.images[face_indices[i]], cmap=plt.cm.bone)
        p.text(0, 14, text)
        p.text(0, 60, str(i))
        p.axis('off')

# button_no_smile.on_click(update_no_smile)
# button_smile.on_click(update_smile)

# display(button_smile)
# display(button_no_smile)
# display_face(trainer.imgs[trainer.index])            

# results = json.load(open('results.xml'))
# trainer.results = results

# with open('results.xml', 'w') as f:
#    json.dump(trainer.results, f)

# yes, no = (sum([trainer.results[x] == True for x in trainer.results]), sum([trainer.results[x] == False for x in trainer.results]))
# bar([0, 1], [no, yes])
# ylim(0, max(yes, no))
# xticks([0.4, 1.4], ['no smile', 'smile']);

# plt_figure(True,"smiling")
# plt_figure(False,"not smiling")

# svc_1 = SVC(kernel='linear')
# indices = [i for i in trainer.results]
# data = faces.data[indices, :]
# target = [trainer.results[i] for i in trainer.results]
# target = array(target).astype(int32)

# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state=0)

# def evaluate_cross_validation(clf, X, y, K):
#     cv = KFold(len(y), K, shuffle=True, random_state=0)
#     scores = cross_val_score(clf, X, y, cv=cv)
#     print (scores)
#     print ("Mean score: {0:.3f} (+/-{1:.3f})".format(np.mean(scores), sem(scores)))

# evaluate_cross_validation(svc_1, X_train, y_train, 5)

# def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
#     clf.fit(X_train, y_train)
#     print ("Accuracy on training set:")
#     print (clf.score(X_train, y_train))
#     print ("Accuracy on testing set:")
#     print (clf.score(X_test, y_test))
#     y_pred = clf.predict(X_test)
#     print ("Classification Report:")
#     print (metrics.classification_report(y_test, y_pred))
#     print ("Confusion Matrix:")
#     print (metrics.confusion_matrix(y_test, y_pred))

# train_and_evaluate(svc_1, X_train, X_test, y_train, y_test)    

# random_image_button = ButtonWidget(description="New image!")

# def display_face_and_prediction(b):
#     index = randint(0, 400)
#     face = faces.images[index]
#     display_face(face)
#     print("this person is smiling: {0}".format(svc_1.predict(faces.data[index, :])==1))

# input_face = cv2.imread('face6.jpg')
# cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
# faceCascade = cv2.CascadeClassifier(cascPath)
# gray = cv2.cvtColor(input_face, cv2.COLOR_BGR2GRAY)
# detected_faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=6,minSize=(100, 100),flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
# detected_faces

# ax = gca()
# ax.imshow(gray, cmap='gray')
# for (x, y, w, h) in detected_faces:
#     ax.add_artist(Rectangle((x, y), w, h, fill=False, lw=5, color='blue'))

# original_extracted_face = gray[y:y+h, x:x+w]
# horizontal_offset = 0.15 * w
# vertical_offset = 0.2 * h
# extracted_face = gray[y+vertical_offset:y+h, x+horizontal_offset:x-horizontal_offset+w]

# subplot(121)
# imshow(original_extracted_face, cmap='gray')
# subplot(122)
# imshow(extracted_face, cmap='gray')

# new_extracted_face = zoom(extracted_face, (64. / extracted_face.shape[0], 64. / extracted_face.shape[1]))
# new_extracted_face = new_extracted_face.astype(float32)
# new_extracted_face /= float(new_extracted_face.max())
# display_face(new_extracted_face[:, :])

# svc_1.predict(new_extracted_face.ravel())

# def detect_face(frame):
#     cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
#     faceCascade = cv2.CascadeClassifier(cascPath)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     detected_faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50))
#     return gray, detected_faces

# def extract_face_features(gray, detected_face, offset_coefficients):
#     (x, y, w, h) = detected_face
#     horizontal_offset = offset_coefficients[0] * w
#     vertical_offset = offset_coefficients[1] * h
#     extracted_face = gray[y+vertical_offset:y+h, x+horizontal_offset:x-horizontal_offset+w]
#     new_extracted_face = zoom(extracted_face, (64. / extracted_face.shape[0], 64. / extracted_face.shape[1]))
#     new_extracted_face = new_extracted_face.astype(float32)
#     new_extracted_face /= float(new_extracted_face.max())
#     return new_extracted_face

# def predict_face_is_smiling(extracted_face):
#     return svc_1.predict(extracted_face.ravel())

# subplot(121)
# imshow(cv2.cvtColor(cv2.imread('face5.jpg'), cv2.COLOR_BGR2GRAY), cmap='gray')
# subplot(122)
# imshow(cv2.cvtColor(cv2.imread('face6.jpg'), cv2.COLOR_BGR2GRAY), cmap='gray')

# gray1, face1 = detect_face(cv2.imread("face5.jpg"))
# gray2, face2 = detect_face(cv2.imread("face6.jpg"))

# def test_recognition(c1, c2):
#     subplot(121)
#     extracted_face1 = extract_face_features(gray1, face1[0], (c1, c2))
#     imshow(extracted_face1, cmap='gray')
#     print(predict_face_is_smiling(extracted_face1))
#     subplot(122)
#     extracted_face2 = extract_face_features(gray2, face2[0], (c1, c2))
#     imshow(extracted_face2, cmap='gray')
#     print(predict_face_is_smiling(extracted_face2))

# interact(test_recognition,c1=(0.0, 0.3, 0.01),c2=(0.0, 0.3, 0.01))

# def make_map(facefile):
#     c1_range = linspace(0, 0.35)
#     c2_range = linspace(0, 0.3)
#     result_matrix = nan * zeros_like(c1_range * c2_range[:, newaxis])
#     gray, detected_faces = detect_face(cv2.imread(facefile))
#     for face in detected_faces[:1]:
#         for ind1, c1 in enumerate(c1_range):
#             for ind2, c2 in enumerate(c2_range):
#                 extracted_face = extract_face_features(gray, face, (c1, c2))
#                 result_matrix[ind1, ind2] = predict_face_is_smiling(extracted_face)
#     return (c1_range, c2_range, result_matrix)

# r1 = make_map("face5.jpg")
# r2 = make_map("face6.jpg")

# figure(figsize=(12, 4))
# subplot(131)
# title('not smiling image')
# pcolormesh(r1[0], r1[1], r1[2])
# colorbar()
# xlabel('horizontal stretch factor c1')
# ylabel('vertical stretch factor c2')

# subplot(132)
# title('smiling image')
# pcolormesh(r2[0], r2[1], r2[2])
# colorbar()
# xlabel('horizontal stretch factor c1')
# ylabel('vertical stretch factor c2')

# subplot(133)
# title('correct settings for both images simultaneously')
# pcolormesh(r1[0], r1[1], (r1[2]==0) & (r2[2]==1), cmap='gray')
# colorbar()
# xlabel('horizontal stretch factor c1')
# ylabel('vertical stretch factor c2')

# tight_layout()


# extracted_faces = []
# for facefile in ["face5.jpg", "face6.jpg"]:
#     gray, detected_faces = detect_face(cv2.imread(facefile))
#     for face in detected_faces:
#         extracted_face = extract_face_features(gray, face, offset_coefficients=(0.03, 0.05))
#         extracted_faces.append(extracted_face)
        
# imshow(mean(array(extracted_faces), axis=0), cmap='gray')                         

# def live_cam():
#     cascPath = 'C:\Users\DELL\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
#     faceCascade = cv2.CascadeClassifier(cascPath)
#     video_capture = cv2.VideoCapture(0)
#     while True:
#         ret, frame = video_capture.read()
#         gray, detected_faces = detect_face(frame)
#         face_index = 0
#         for face in detected_faces:
#             (x, y, w, h) = face
#             if w > 100:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#                 extracted_face = extract_face_features(gray, face, (0.03, 0.05)) #(0.075, 0.05)
#                 prediction_result = predict_face_is_smiling(extracted_face)
#                 frame[face_index * 64: (face_index + 1) * 64, -65:-1, :] = cv2.cvtColor(extracted_face * 255, cv2.COLOR_GRAY2RGB)
#                 if prediction_result == 1: cv2.putText(frame, "SMILING",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)
#                 else: cv2.putText(frame, "not smiling",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)
#                 face_index += 1
#         cv2.imshow('Video', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'): break

#     video_capture.release()
#     cv2.destroyAllWindows()

# live_cam()    