#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    words = []
    for line in lines:
        temp = line.split(", ")[0]
        words.extend(temp.split())
    lst = [[int(token) for token in line.split(", ")[1:]] for line in lines]
    M = np.array(lst)
    x_positive = M[:, 0:-1]
    y_positive = M[:, -1:]
    return x_positive, y_positive

if __name__ == "__main__":
    x_positive, y_positive = read_file("positive.dat")
    x_negative, y_negative = read_file("negative_pruned.dat")
    n_positive = x_positive.shape[0]
    x_train = np.vstack((x_positive, x_negative))
    y_train = np.vstack((y_positive, y_negative))
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    positive_predict = clf.predict(x_positive)
    nTP = positive_predict.sum()
    train_predict = clf.predict(x_train)
    nP = train_predict.sum()
    print("recall = {:0.6f} %".format(nTP / n_positive * 100.0))
    print("presison = {:0.6f} %".format(nTP / nP * 100.0))
