import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from csv import DictReader, DictWriter
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from collections import Counter
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import ClusterCentroids
from sklearn.ensemble import RandomForestClassifier
from scipy.optimize import minimize
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sklearn.neural_network import MLPClassifier
# import some data to play with
X = []
Y = []
reader = DictReader(open("picture.csv", 'r'))
for row in reader:
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
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.25, random_state=0)
### building the classifiers
clfs = []

svc = SVC(kernel="linear", C=0.025,probability=True)
svc.fit(train_x, train_y)
print('SVC LogLoss {score}'.format(score=log_loss(test_y, svc.predict_proba(test_x))))
clfs.append(svc)

svc = SVC(kernel="linear", C=0.025,probability=True)
svc.fit(train_x, train_y)
print('SVC LogLoss {score}'.format(score=log_loss(test_y, svc.predict_proba(test_x))))
clfs.append(svc)

rfc = RandomForestClassifier(n_estimators=50, random_state=4141, n_jobs=-1)
rfc.fit(train_x, train_y)
print('RFC LogLoss {score}'.format(score=log_loss(test_y, rfc.predict_proba(test_x))))
clfs.append(rfc)

sgd = SGDClassifier(loss='log', penalty='l2', shuffle=True)
sgd.fit(train_x, train_y)
print('SGDClassifier LogLoss {score}'.format(score=log_loss(test_y, sgd.predict_proba(test_x))))
clfs.append(sgd)

### finding the optimum weights

predictions = []
for clf in clfs:
    predictions.append(clf.predict_proba(test_x))

def log_loss_func(weights):
    ''' scipy minimize will pass the weights as a numpy array '''
    final_prediction = 0
    for weight, prediction in zip(weights, predictions):
            final_prediction += weight*prediction

    return log_loss(test_y, final_prediction)
    
starting_values = [0.5]*len(predictions)

cons = ({'type':'eq','fun':lambda w: 1-sum(w)})
bounds = [(0,1)]*len(predictions)

res = minimize(log_loss_func, starting_values, method='SLSQP', bounds=bounds, constraints=cons)

print('Ensamble Score: {best_score}'.format(best_score=res['fun']))
print('Best Weights: {weights}'.format(weights=res['x']))
