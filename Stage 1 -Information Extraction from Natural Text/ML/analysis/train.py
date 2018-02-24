#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import svm
from sklearn import linear_model

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    words = []
    for line in lines:
        temp = line.split(", ")[0]
        words.extend(temp.split())
    lst = [[int(token) for token in line.split(", ")[1:]] for line in lines]
    M = np.array(lst)
    x = M[:, 0:-1]
    y = M[:, -1:]
    return x, y

def train_and_test(clf, name):
    train_x_positive, train_y_positive = read_file("positive.dat")
    train_x_negative, train_y_negative = read_file("negative_pruned.dat")
    train_n_positive = train_x_positive.shape[0] # number of positive samples
    train_x = np.vstack((train_x_positive, train_x_negative))
    train_y = np.vstack((train_y_positive, train_y_negative))
    clf.fit(train_x, train_y.ravel())
    train_positive_predict = clf.predict(train_x_positive)
    nTP = train_positive_predict.sum() # true positive
    train_predict = clf.predict(train_x)
    nP = train_predict.sum() # positive
    train_recall, train_precision = nTP / train_n_positive * 100.0, nTP / nP * 100.0
    print(name, "train recall = {:0.6f} %".format(train_recall))
    print(name, "train presison = {:0.6f} %".format(train_precision))
    print(name, "train F1-score = {:0.6f} %".format(2 * (train_precision * train_recall) / (train_precision
    + train_recall)))
    test_x_positive, test_y_positive = read_file("test_positive.dat")
    test_x_negative, test_y_negative = read_file("test_negative_pruned.dat")
    test_x = np.vstack((test_x_positive, test_x_negative))
    test_predict = clf.predict(test_x)
    test_positive_predict = clf.predict(test_x_positive)
    nP = test_predict.sum()
    nTP = test_positive_predict.sum()
    test_recall, test_precision = nTP / test_x_positive.shape[0] * 100.0, nTP / nP * 100.0
    print("=====================================================")
    print(name, "test recall = {:0.6f} %".format(test_recall))
    print(name, "test precision = {:0.6f} %".format(test_precision))
    print(name, "test F1-score = {:0.6f} %".format(2 * (test_precision * test_recall) / (test_precision +
    test_recall)))
    print ("\n")

if __name__ == "__main__":
    
    # use decision tree classifier
    dt_clf = tree.DecisionTreeClassifier()
    train_and_test(dt_clf, "decision_tree")
    # use svm classifier
    svm_clf = svm.SVC()
    train_and_test(svm_clf, "SVM")
    # use logisticRegression
    lr_clf = linear_model.LogisticRegression()
    train_and_test(lr_clf, "logistic_regression")
