import numpy as np
import matplotlib.pyplot as plt
from csv import DictReader, DictWriter
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from collections import Counter
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import ClusterCentroids
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

names = ["SGDClassifier","Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

classifiers = [
	SGDClassifier(loss='log', penalty='l2', shuffle=True),
    KNeighborsClassifier(7),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(n_estimators=50, random_state=4141, n_jobs=-1),
    MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]
# import some data to play with
X = []
Y = []
reader = DictReader(open("Cinematography.csv", 'r'))
for idx,row in enumerate(reader):
	if idx > 400 and row['win'] == '0':
		continue
	Y.append(row['win'])
	del row['win']
	X.append(row)
v = DictVectorizer(sparse=False)
X = v.fit_transform(X)
print('Original dataset shape {}'.format(Counter(Y)))
#sm = SMOTE(kind='svm')
sm = ClusterCentroids(random_state=42)
X, Y = sm.fit_sample(X, Y)
print('Resampled dataset shape {}'.format(Counter(Y)))
precisions = []
recalls = []
mathews_coefficients = []
accuracy_scores = []
for name, clf in zip(names, classifiers):
	print name
	predicted = cross_val_predict(clf, X, Y, cv=3,n_jobs=7,verbose=1)
	accurancy = accuracy_score(Y, predicted)
	precision = precision_score(Y, predicted, average='micro')
	recall = recall_score(Y, predicted, average='micro')
	matthews = matthews_corrcoef(Y, predicted)
	precisions.append(precision)
	recalls.append(recall)
	mathews_coefficients.append(matthews)
	accuracy_scores.append(accurancy)
	print (accurancy,matthews)
	print(classification_report(Y, predicted))
	
for indx,name in enumerate(names):
	print (name,precisions[indx],recalls[indx],accuracy_scores[indx],mathews_coefficients[indx])
