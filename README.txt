Run the main.py file
    - The main.py file has calls to all the 5 algorithms implemented.
    - We are reading the data from "toy_data.csv" file which has around 500 records which is been taken from the Preprocessed data.

##################
preprocess_main.py file:
    - This file does the preprocessing of data by reading the "final_imdb.csv" file which contains about 5389 records.
    - The pre-processed data is stored in preprocess.csv file
    - Our algorithms are run on "preprocess.csv" data and the accuracies which are obtained on this dataset is been indicated in the report file.

###############
toy_data.csv file:
    - This file is 15% of the "preprocess.csv" file. We used the train_test_split method to split the dataset.

DataVisualization.py:
    - This file is called from "Preprocess.py" file. This call is currently commented. This was used to visualize the correlations of data.

ScrapeData.py:
    - This was used to scrape data from IMDB.

NaiveBAlg.py:
    - This file has code to run the Naive Bayes algorithm. Here the gaussian principle is used. So we calculate mean and standard deviations for each features to predict the test data.

DecisionTreeClassifier.py:
    - This file contains the implementation of C4.5 Decision trees algorithm.

SVM.py:
    - This file contains the implementation for SVM algorithm.

knn.py:
    - This file contains the implementation for KNN algorithm.

LogisticRegression.py:
    - This file contains the implementation for Logistic regression algorithm.