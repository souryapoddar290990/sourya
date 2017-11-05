import numpy as np
# from collections import Counter
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import cross_validation
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# from sklearn.linear_model import LogisticRegression, LinearRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.naive_bayes import GaussianNB
# from sklearn.svm import SVC
# from sklearn.decomposition import PCA
# from sklearn import datasets
# from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MeanShift
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
# from sklearn.neural_network import MLPClassifier
# from scipy.cluster import hierarchy
# from mpl_toolkits.mplot3d import Axes3D
import csv
# import pprint
# import seaborn as sns

# reading sensor files
def preprocess(sensor_file, label_file):
	sensor = pd.read_csv(sensor_file)
	lbl = pd.read_csv(label_file)
	lbl.rename(columns={'label (0=start 1=end 2=cancel)': 'shake'}, inplace=True)
	# merge two files based on timestamp
	new_data = sensor.merge(lbl, how='outer', left_on="timestamp(ms)", right_on="timestamp(ms)")
	new_data = new_data.sort(columns="timestamp(ms)")
	new_data.iloc[-1,10] = 0
	# define shake as new column, 1 represents shake and 0 represents no shake
	new_data["shake"] = new_data["shake"].bfill()
	new_data = new_data.dropna(how='any')
	# print new_data["shake"].sum()
	# print new_data.describe()
	return new_data

a_new_data = preprocess("a.sensor.csv","a.lbl.csv")
m_new_data = preprocess("m.sensor.csv","m.lbl.csv")
p_new_data = preprocess("p.sensor.csv","p.lbl.csv")

# merge all 3 sensor files
main_data = a_new_data
main_data = main_data.append(m_new_data)
main_data = main_data.append(p_new_data)

# prepare dataset
label = main_data[1:]['shake']
data = main_data[1:][['timestamp(ms)', 'acceleration_x(g)', 'acceleration_y(g)', 'acceleration_z(g)', 'roll(rad)', 'pitch(rad)', 'yaw(rad)', 'angular_velocity_x(rad/sec)', 'angular_velocity_y(rad/sec)', 'angular_velocity_z(rad/sec)']]

# define new features
main_data['derived1'] = (main_data['acceleration_x(g)']*main_data['acceleration_x(g)']+main_data['acceleration_y(g)']*main_data['acceleration_y(g)']+main_data['acceleration_z(g)']*main_data['acceleration_z(g)']).apply(np.sqrt)
main_data['derived2'] = (main_data['angular_velocity_x(rad/sec)']*main_data['angular_velocity_x(rad/sec)']+main_data['angular_velocity_y(rad/sec)']*main_data['angular_velocity_y(rad/sec)']+main_data['angular_velocity_z(rad/sec)']*main_data['angular_velocity_z(rad/sec)']).apply(np.sqrt)

# compute consecutive row difference
main_data_diff = main_data[['timestamp(ms)','acceleration_x(g)','acceleration_y(g)','acceleration_z(g)','angular_velocity_x(rad/sec)','angular_velocity_y(rad/sec)','angular_velocity_z(rad/sec)','roll(rad)','pitch(rad)','yaw(rad)','derived1','derived2']].set_index('timestamp(ms)').diff()

# pairwise corelation check and drop angular_velocity_y(rad/sec) as it has high correlation with angular_velocity_x(rad/sec)
correlation = main_data.corr(method='pearson').abs()
np.fill_diagonal(correlation.values, -2)
correlation = correlation.unstack().sort_values()
# print correlation

# prepare data for classification
data = main_data_diff[1:]
datas = pd.DataFrame(data[['acceleration_x(g)','acceleration_y(g)','acceleration_z(g)','angular_velocity_x(rad/sec)','angular_velocity_z(rad/sec)','roll(rad)','pitch(rad)','yaw(rad)','derived1','derived2']])

#random sampling 80:20 split for train and test dataset
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(datas, label, test_size=0.2)

print sum(Y_test),len(Y_test)-sum(Y_test),sum(Y_train),len(Y_train)-sum(Y_train)
# fitting random forest
random_forest = RandomForestClassifier(n_estimators=5)
random_forest.fit(X_train, Y_train)
print random_forest.fit(X_train, Y_train).feature_importances_
print "TRAIN ACCURACY : ",random_forest.score(X_train, Y_train)

# testing accuracy
# Y_pred = random_forest.predict_proba(X_test)
# y_pred = random_forest.predict(X_train)
# mis_classification = (Y_train != y_pred).sum()
# accuracy = 1-mis_classification/float(len(Y_train))
# print "TRAIN ACCURACY : ",accuracy
# a,b,c,d = 0,0,0,0
# for index,item in enumerate(y_pred):
# 	if Y_train.iloc[index] == 0.0 and item == 0.0: a += 1
# 	if Y_train.iloc[index] == 0.0 and item == 1.0: b += 1
# 	if Y_train.iloc[index] == 1.0 and item == 0.0: c += 1
# 	if Y_train.iloc[index] == 1.0 and item == 1.0: d += 1
# print a,b,c,d

y_pred = random_forest.predict(X_test)
mis_classification = (Y_test != y_pred).sum()
accuracy = 1-mis_classification/float(len(Y_test))
print "TEST ACCURACY : ",accuracy
# for index,item in enumerate(y_pred):
	# if Y_test.iloc[index] != item: print Y_test.iloc[index],Y_pred[index],item
	# else: print Y_test.iloc[index], item
# a,b,c,d = 0,0,0,0
# for index,item in enumerate(y_pred):
# 	if Y_test.iloc[index] == 0.0 and item == 0.0: a += 1
# 	if Y_test.iloc[index] == 0.0 and item == 1.0: b += 1
# 	if Y_test.iloc[index] == 1.0 and item == 0.0: c += 1
# 	if Y_test.iloc[index] == 1.0 and item == 1.0: d += 1
# print a,b,c,d

tp,tn,fp,fn = 211.0,32210.0,302.0,51.0
precision = tp/(tp+fp)
recall = tp/(tp+fn)
print precision, recall