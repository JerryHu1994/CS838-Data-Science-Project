#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang, Jieru Hu
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import svm
from sklearn import linear_model
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
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

# cross-validation on the train set
def cv(clf, name):
    train_x_positive, train_y_positive = read_file("positive.dat")
    train_x_negative, train_y_negative = read_file("negative_pruned.dat")
    train_n_positive = train_x_positive.shape[0] # number of positive samples
    train_x = np.vstack((train_x_positive, train_x_negative))
    train_y = np.vstack((train_y_positive, train_y_negative))
    # shuffle the positive and negative sets
    shuffled_x, shuffled_y = shuffle(train_x, train_y, random_state=0)
    kf = KFold(n_splits=4)
    nTP, nP = 0, 0
    for train_index, test_index in kf.split(shuffled_x):
        kf_x_train, kf_x_test = shuffled_x[train_index], shuffled_x[test_index]
        kf_y_train, kf_y_test = shuffled_y[train_index], shuffled_y[test_index]
        #train the classifier
        clf.fit(kf_x_train, kf_y_train.ravel())
        test_predict = clf.predict(kf_x_test)
        nP += test_predict.sum()
        # extract text_positives
        kf_x_test_positive = kf_x_test[np.where(kf_y_test==1)[0]]
        test_predict_positive = clf.predict(kf_x_test_positive)
        nTP += test_predict_positive.sum()
        
    train_precision = nTP / nP * 100.0
    print(name, "Cross-Validation presison = {:0.6f} %".format(train_precision))
    return train_precision

def train_and_test(clf, name):
    train_x_positive, train_y_positive = read_file("positive.dat")
    train_x_negative, train_y_negative = read_file("negative_pruned.dat")
    train_n_positive = train_x_positive.shape[0] # number of positive samples
    train_x = np.vstack((train_x_positive, train_x_negative))
    train_y = np.vstack((train_y_positive, train_y_negative))
    # shuffle the positive and negative sets
    shuffled_x, shuffled_y = shuffle(train_x, train_y, random_state=0)
    clf.fit(shuffled_x, shuffled_y.ravel())
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
    # use svm classifier
    svm_clf = svm.SVC()
    # use logisticRegression
    lor_clf = linear_model.LogisticRegression()
    rf_clf = RandomForestClassifier(max_depth=2, random_state=0)
    lir_clf = linear_model.LinearRegression()
    clf_list = [dt_clf, svm_clf, lor_clf, rf_clf, lir_clf]
    clf_name = ["Decision Tree", "SVM", "Logistic Regression", "Random Forest", "Linear Regression"]
    precisions = []
    for ind, clf in enumerate(clf_list):
        precisions.append(cv(clf, clf_name[ind]))
    max_precision = max(precisions)
    max_ind = precisions.index(max_precision)
    best_clf, best_clf_name = clf_list[max_ind], clf_name[max_ind]
    print ("\n")
    print (best_clf_name, "has the best cross-validation precision equal to {:0.6f} %".format(max_precision))
    # let's do the real train and test'
    train_and_test(best_clf, best_clf_name)

