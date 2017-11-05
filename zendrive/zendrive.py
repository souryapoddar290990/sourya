import numpy as np
from collections import Counter
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn import datasets
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MeanShift
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from scipy.cluster import hierarchy
from mpl_toolkits.mplot3d import Axes3D
import csv
import pprint
import seaborn as sns

def preprocess(sensor_file, label_file):
	sensor = pd.read_csv(sensor_file)
	lbl = pd.read_csv(label_file)
	lbl.rename(columns={'label (0=start 1=end 2=cancel)': 'shake'}, inplace=True)
	new_data = sensor.merge(lbl, how='outer', left_on="timestamp(ms)", right_on="timestamp(ms)")
	new_data = new_data.sort(columns="timestamp(ms)")
	new_data.iloc[-1,10] = 0
	new_data["shake"] = new_data["shake"].bfill()
	new_data = new_data.dropna(how='any')
	# print new_data["shake"].sum()
	# print new_data.describe()
	return new_data

a_new_data = preprocess("a.sensor.csv","a.lbl.csv")
m_new_data = preprocess("m.sensor.csv","m.lbl.csv")
p_new_data = preprocess("p.sensor.csv","p.lbl.csv")

main_data = a_new_data
main_data = main_data.append(m_new_data)
main_data = main_data.append(p_new_data)

# posi = main_data[main_data.shake > 0]
# posi.to_csv('posi.csv')
# datap = pd.read_csv('posi.csv')
# nege = main_data[main_data.shake < 1]
# nege.to_csv('nege.csv')
# datan = pd.read_csv('nege.csv')

# datap['derived'] = abs(datap['angular_velocity_x(rad/sec)'])+abs(datap['angular_velocity_y(rad/sec)'])+abs(datap['angular_velocity_z(rad/sec)'])
# datan['derived'] = abs(datan['angular_velocity_x(rad/sec)'])+abs(datan['angular_velocity_y(rad/sec)'])+abs(datan['angular_velocity_z(rad/sec)'])
# print datap.describe()

label = main_data[1:]['shake']
data = main_data[1:][['timestamp(ms)', 'acceleration_x(g)', 'acceleration_y(g)', 'acceleration_z(g)', 'roll(rad)', 'pitch(rad)', 'yaw(rad)', 'angular_velocity_x(rad/sec)', 'angular_velocity_y(rad/sec)', 'angular_velocity_z(rad/sec)']]
main_data['derived1'] = abs(main_data['acceleration_x(g)'])+abs(main_data['acceleration_y(g)'])+abs(main_data['acceleration_z(g)'])
main_data['derived2'] = abs(main_data['angular_velocity_x(rad/sec)'])+abs(main_data['angular_velocity_x(rad/sec)'])+abs(main_data['angular_velocity_x(rad/sec)'])
# main_data['derived3'] = main_data[['acceleration_x(g)','acceleration_y(g)','acceleration_z(g)']].max(axis=1)
# main_data['derived4'] = abs(main_data['acceleration_x(g)'])*abs(main_data['angular_velocity_x(rad/sec)'])+abs(main_data['acceleration_y(g)'])*abs(main_data['angular_velocity_y(rad/sec)'])+abs(main_data['acceleration_z(g)'])*abs(main_data['angular_velocity_z(rad/sec)'])
# main_data['derived5'] = main_data['acceleration_x(g)']*main_data['acceleration_x(g)']+main_data['acceleration_y(g)']*main_data['acceleration_y(g)']+main_data['acceleration_z(g)']*main_data['acceleration_z(g)']
# main_data['derived6'] = main_data['angular_velocity_x(rad/sec)']*main_data['angular_velocity_x(rad/sec)']+main_data['angular_velocity_y(rad/sec)']*main_data['angular_velocity_y(rad/sec)']+main_data['angular_velocity_z(rad/sec)']*main_data['angular_velocity_z(rad/sec)']
# main_data['derived7'] = main_data['acceleration_x(g)']
main_data['derived8'] = (main_data['acceleration_x(g)']*main_data['acceleration_x(g)']+main_data['acceleration_y(g)']*main_data['acceleration_y(g)']+main_data['acceleration_z(g)']*main_data['acceleration_z(g)']).apply(np.sqrt)+(main_data['angular_velocity_x(rad/sec)']*main_data['angular_velocity_x(rad/sec)']+main_data['angular_velocity_y(rad/sec)']*main_data['angular_velocity_y(rad/sec)']+main_data['angular_velocity_z(rad/sec)']*main_data['angular_velocity_z(rad/sec)']).apply(np.sqrt)+abs(main_data['roll(rad)'])+abs(main_data['pitch(rad)'])+abs(main_data['yaw(rad)'])

main_data_diff = main_data[['timestamp(ms)','acceleration_x(g)','acceleration_y(g)','acceleration_z(g)','angular_velocity_x(rad/sec)','angular_velocity_y(rad/sec)','angular_velocity_z(rad/sec)','roll(rad)','pitch(rad)','yaw(rad)']].set_index('timestamp(ms)').diff()
main_data_diff['derived1'] = abs(main_data_diff['acceleration_x(g)'])+abs(main_data_diff['acceleration_y(g)'])+abs(main_data_diff['acceleration_z(g)'])
main_data_diff['derived2'] = abs(main_data_diff['angular_velocity_x(rad/sec)'])+abs(main_data_diff['angular_velocity_x(rad/sec)'])+abs(main_data_diff['angular_velocity_x(rad/sec)'])
main_data_diff['derived8'] = (main_data_diff['acceleration_x(g)']*main_data_diff['acceleration_x(g)']+main_data_diff['acceleration_y(g)']*main_data_diff['acceleration_y(g)']+main_data_diff['acceleration_z(g)']*main_data_diff['acceleration_z(g)']).apply(np.sqrt)+((main_data_diff['angular_velocity_x(rad/sec)'])*main_data_diff['angular_velocity_x(rad/sec)']+main_data_diff['angular_velocity_y(rad/sec)']*main_data_diff['angular_velocity_y(rad/sec)']+main_data_diff['angular_velocity_z(rad/sec)']*main_data_diff['angular_velocity_z(rad/sec)']).apply(np.sqrt)+abs(main_data_diff['roll(rad)'])+abs(main_data_diff['pitch(rad)'])+abs(main_data_diff['yaw(rad)'])
# print main_data_diff[1:].info()
# print main_data[1:]['shake'].describe()
correlation = main_data.corr(method='pearson')
print correlation
# f, ax = plt.subplots(figsize=(11, 9))
# cmap = sns.diverging_palette(220, 10, as_cmap=True)
# mask = np.zeros_like(correlation, dtype=np.bool)
# mask[np.triu_indices_from(mask)] = True
# sns.heatmap(correlation, mask=mask, cmap=cmap, vmax=.3, square=True, xticklabels=5, yticklabels=5, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
# sns.factorplot('shake','derived8', data=main_data,size=4,aspect=3)
# plt.show()
# print main_data_diff.describe()
# posi = main_data[main_data.shake > 0]
# posi.to_csv('posi.csv')
# datap = pd.read_csv('posi.csv')
# nege = main_data[main_data.shake < 1]
# nege.to_csv('nege.csv')
# datan = pd.read_csv('nege.csv')
# print posi.describe()
# print nege.describe()



def LOGISTIC_REGRESSION(X_train, X_test, Y_train, Y_test):
	lor = LogisticRegression()
	y_pred = lor.fit(X_train, Y_train).predict(X_test)
	# print lor.fit(X_train, Y_train).coef_
	print Y_test.sum(),sum(y_pred)
	accuracy = (Y_test != y_pred).sum()
	return accuracy
def K_NEAREST_NEIGHBOURS(X_train, X_test, Y_train, Y_test, k):
	knn = KNeighborsClassifier(n_neighbors=k)
	y_pred = knn.fit(X_train, Y_train).predict(X_test)
	accuracy = (Y_test != y_pred).sum()
	tp,pp = 0,0
	for index,item in enumerate(y_pred):
		if Y_test.iloc[index] == 1.0:
			tp += 1
			if item == 1.0: pp += 1
		# pass
	print pp/float(tp),tp-pp
	return accuracy
def DECISION_TREE(X_train, X_test, Y_train, Y_test):
	det = DecisionTreeClassifier()
	y_pred = det.fit(X_train, Y_train).predict(X_test)
	tp,pp = 0,0
	for index,item in enumerate(y_pred):
		if Y_test.iloc[index] == 1.0:
			tp += 1
			if item == 1.0: pp += 1
		# pass
	print pp/float(tp),tp-pp
	accuracy = (Y_test != y_pred).sum()
	return accuracy
def BAGGING(X_train, X_test, Y_train, Y_test, model):
	bag = BaggingClassifier(base_estimator=model, n_estimators=10, bootstrap=True)
	y_pred = bag.fit(X_train, Y_train).predict(X_test)
	accuracy = (Y_test != y_pred).sum()
	tp,pp = 0,0
	for index,item in enumerate(y_pred):
		if Y_test.iloc[index] == 1.0:
			tp += 1
			if item == 1.0: pp += 1
		# pass
	print pp/float(tp),tp-pp	
	return accuracy
def RANDOM_FOREST(X_train, X_test, Y_train, Y_test):
	rfr = RandomForestClassifier(n_estimators=100, criterion='gini', bootstrap=True)
	y_pred = rfr.fit(X_train, Y_train).predict(X_test)
	accuracy = (Y_test != y_pred).sum()
	# print rfr.fit(X_train, Y_train).feature_importances_
	tp,pp = 0,0
	for index,item in enumerate(y_pred):
		if Y_test.iloc[index] == 1.0:
			tp += 1
			if item == 1.0: pp += 1
		# pass
	print pp/float(tp),tp-pp	
	return accuracy

# label = main_data[2:]['shake']
# main_data_diff['labels'] = pd.Series(label)
# print main_data_diff.columns
data = main_data[1:]
# print data.columns
datas = pd.DataFrame(data[['acceleration_x(g)','acceleration_y(g)','acceleration_z(g)','angular_velocity_x(rad/sec)','angular_velocity_y(rad/sec)','angular_velocity_z(rad/sec)','roll(rad)','pitch(rad)','yaw(rad)','derived8']])
# print datas
# print label
# datas = dts[~((dts-dts.mean()).abs()>3*dts.std())]
# rows = ~((dts-dts.mean()).abs()>3*dts.std())

# datas = dts[~(np.abs(dts.derived1-dts.derived1.mean())>(3*dts.derived1.std()))]
# print datas.describe()

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(datas, label, test_size=0.2)

# logreg = LogisticRegression()
# logreg.fit(X_train, Y_train)
# Y_pred = logreg.predict(X_test)
# print logreg.score(X_train, Y_train)

random_forest = RandomForestClassifier(n_estimators=1)
random_forest.fit(X_train, Y_train)
print random_forest.fit(X_train, Y_train).feature_importances_
Y_pred = random_forest.predict_proba(X_test)
y_pred = random_forest.predict(X_test)
# print y_pred
for index,item in enumerate(y_pred):
	if Y_test.iloc[index] != item: print Y_test.iloc[index],Y_pred[index],item
	# else: print Y_test.iloc[index], item

# print random_forest.score(X_train, Y_train)

# print len(Y_test),len(Y_train),len(X_test),len(X_train)


def mixed(X_train, X_test, Y_train, Y_test):
	lor = LogisticRegression()
	y_pred1 = lor.fit(X_train, Y_train).predict(X_test)	
	det = DecisionTreeClassifier()
	y_pred2 = det.fit(X_train, Y_train).predict(X_test)
	knn = KNeighborsClassifier(n_neighbors=5)
	y_pred3 = knn.fit(X_train, Y_train).predict(X_test)
	y_pred = y_pred1+y_pred2+y_pred3
	tp,pp,pp1,pp2,pp3 = 0,0,0,0,0
	for index,item in enumerate(y_pred):
		if Y_test.iloc[index] == 1.0:
			tp += 1
			if item > 0.0:
				# print ">>>>>>>>>>>>>>>>>",X_test.iloc[index]['derived8']
				pp += 1
			# else: print X_test.iloc[index]['derived8']
		# pass
	print pp/float(tp),tp-pp
	# accuracy = (Y_test != y_pred).sum()
	# return accuracy

# print mixed(X_train, X_test, Y_train, Y_test)

# a,b = [],[]
# for index in range(len(X_train)):
# 	if Y_train.iloc[index] == 0:
# 		a.append(X_train.iloc[index])
# 	else:
# 		b.append(X_train.iloc[index])
# temp_a = np.mean(a)+np.std(a)
# temp_b = np.mean(b)-np.std(b)
# print temp_a,temp_b,(temp_a+temp_b)/2.0

# y_pred = []
# for index in range(len(X_test)):
# 	if X_test['derived8'].iloc[index] > 1.74210818632:
# 		y_pred.append(1)
# 	else:
# 		y_pred.append(0)


# tp,pp = 0,0
# for index,item in enumerate(y_pred):
# 	if Y_test.iloc[index] == 1.0:
# 		tp += 1
# 		if item == 1.0: pp += 1
# 	# pass
# print pp/float(tp),tp-pp,tp


# plt.show()