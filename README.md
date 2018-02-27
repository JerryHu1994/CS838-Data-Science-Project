# CS838-Data-Science-Project
The git repo for CS 838 Data Science in UW-Madison

* Stage 1: [Information extraction from natural text](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-1)
In this project, we build a learning based information extractor which can extract person 
names from natural text documents. The data we used is IMDb users' comments.
Training set contains 1461 positive samples and 1500 negative samples.
Cross validation (with 4 folds) is used to compare performace of random forest, decision tree,
SVM, logistic regression and linear regression. We choose the model with best precision. Test set is
composed of 850 positive samples and 850 negative samples. Oue IE can achieve more than 90 % recall
and more than 92 % precision.

You can call the whole pipeline by running the [bash script](./Stage-1-IE-from-natrual-text/stage1_pipeline.sh)

```
cd Stage-1-IE-from-natural-text
bash stage1_pipeline.sh
```

* Stage 2: [Crawling and extrating structured data from web pages]
