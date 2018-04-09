# CS838-Data-Science-Project
The git repo for CS 838 Data Science in UW-Madison

* **Stage 1**: [Information extraction from natural text](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-1)<br>
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

* **Stage 2**: [Crawling and extrating structured data from web pages](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-2)<br>
In stage 2, we select two two data sources to crawl used car information on the market. One data source is [car.com](https://www.cars.com/), another source comes from APIs provided by [car marketcheck](https://apidocs.marketcheck.com/). We use [beautiful soup](https://www.crummy.com/software/BeautifulSoup/) to crawl used car information from the cars.com page, and use JSON-formatted query to fetch used car data through interacting with the RESTFUL API provided by marketcheck. The used car information is stored into two seperate csv tables for future stage analysis.

You can call the whole pipeline by running the [bash script](./Stage-2-Crawling-structured-Web-data/stage2_pipeline.sh):

```
cd Stage-2-Crawling-structured-Web-data
bash stage2_pipeline.sh
```

* **Stage 3**: [Entity Matching](https://sites.google.com/site/anhaidgroup/courses/cs-838-spring-2018/project-description/stage-3):
In stage 3, we performed entity matching on luxury cars (Mercedes-Benz, BMW, Audi, Lexus) crawded from cars.com and fetched from market check api. The goal is to find same car match betweeen two car data sources. [Magellan](https://sites.google.com/site/anhaidgroup/projects/magellan/py_entitymatching) is the python package used for entity matching in this stage. As a first step, we crawled 3170 cars from cars.com and 2981 cars via Market Check API. The car data is then cleaned and downsampled to a smaller size. Next, blocking is performed to reduce the size of the car-match pair. We applied blocking on attributes including name, year, maker, price, and miles. As a result, the sample candidate car-match pair is reduced from 2622000 to 1532. Last, we run matching on the sample pairs using suprvised learning method. 600 sample pairs is divided into a ratio of 3:1, for training and testing. We used 5-fold cross validation to select the best classifiers from Decision Tree, Random Forest, SVM, Linear Regression and Logistic Regression. Random Forest is selected to be the best classfier. We achieved a precision of 97.01% and a recall of 98.48%.

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




