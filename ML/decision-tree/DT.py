"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree


if __name__ == "__main__":
    iris = load_iris()
    data = iris.data
    target = iris.target
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data, target)
    print(clf.predict(data[:1, :]))
    print(clf.predict_proba(iris.data[:1, :]))
