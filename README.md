# CS838-Data-Science-Project
The git repo for CS 838 Data Science in UW-Madison

* Stage 1: [Information extraction from natural text](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-1)<br>
In this project, we build a learning based information extractor which can extract person 
names from natural text documents. The data we used is IMDb users' comments.
Training set contains 1461 positive samples and 1500 negative samples.
Cross validation (with 4 folds) is used to compare performace of random forest, decision tree,
SVM, logistic regression and linear regression. We choose the model with best precision. Test set is
composed of 850 positive samples and 850 negative samples. Our IE can achieve more than 90 % recall
and more than 92 % precision.

You can call the whole pipeline by running the [bash script](./Stage-1-IE-from-natural-text/stage1_pipeline.sh):

```
cd Stage-1-IE-from-natural-text
bash stage1_pipeline.sh
```

* Stage 2: [Crawling and extrating structured data from web pages](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-2)<br>
In state 2, we select two two data sources to crawl used car information on the market. One data source is [car.com](https://www.cars.com/), another source comes from APIs provided by [car marketcheck](https://apidocs.marketcheck.com/). We use [beautiful soup](https://www.crummy.com/software/BeautifulSoup/) to crawl used car information from the cars.com page, and use JSON-formatted query to fetch used car data through interacting with the RESTFUL API provided by marketcheck. The used car information is stored into two seperate csv tables for future stage analysis.

You can call the whole pipeline by running the [bash script](./Stage-2-Crawling-structured-Web-data/stage2_pipeline.sh):

```
cd Stage-2-Crawling-structured-Web-data
bash stage2_pipeline.sh
```

* Stage 3: [Entity Matching](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-3):

To run the script to crawl luxury cars:
```
cd Stage-3-Entity-Matching/src
bash crawl_luxury_car.sh
```

**Entity Matching Pipeline**

1. Reading two tables from CSV files: [read-csv](Stage-3-Entity-Matching/notebooks/read-csv.ipynb)
2. Down Sampling: [down-sampling](Stage-3-Entity-Matching/notebooks/down-sampling.ipynb)
3. Blocking: [blocking](Stage-3-Entity-Matching/notebooks/block.ipynb)
4. Feature table: [get-features](Stage-3-Entity-Matching/notebooks/features.ipynb)
5. Sampling and labeling
	* Sampling: [sampling](Stage-3-Entity-Matching/notebooks/sample.ipynb)
	* Labeling: [labelling](Stage-3-Entity-Matching/notebooks/label.ipynb)
6. Matching: [matching](Stage-3-Entity-Matching/notebooks/match.ipynb)




