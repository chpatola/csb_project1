import pandas as pd
import pickle
from sklearn import datasets
from sklearn import model_selection
from sklearn import tree

#We will make a cool and fancy ml model here

iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, y, test_size=0.7, random_state=1)

clf = tree.DecisionTreeClassifier()
clf.fit(X, y)

#Using pickle!
filename = 'finalized_model.P'
pickle.dump(clf, open(filename, 'wb'))


