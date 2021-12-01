import Preprocess
import pandas as pd
import numpy as np
from FeatureScaling import FeatureScaling
from NaiveBAlg import NaiveBAlg
from LogisticRegression import LogisticRegression
from sklearn.model_selection import train_test_split
import Evaluation


def get_attribute_list(data):
    return [col for col in data.columns]


def attributeValues(data):
    columns = [col for col in data.columns]
    attr_values = {}
    for column in columns:
        attr_values[column] = list(data[column].value_counts().keys())
    return attr_values


def set_datatype(data):
    data_types = {"runtime": 'int',
                  "budget": 'float',
                  "release_year": 'int'}
    data.astype(data_types)


def set_categorical_type(data):
    col_list = ['runtime', 'budget', 'revenue', 'release_year']
    for col in get_attribute_list(data):
        if col not in col_list:
            data[col] = pd.Categorical(data[col])


def generate_class_label(row):
    if(row['release_day'] == 'Monday'):
        return 1
    if(row['release_day'] == 'Tuesday'):
        return 2
    if(row['release_day'] == 'Wednesday'):
        return 3
    if(row['release_day'] == 'Thursday'):
        return 4
    if(row['release_day'] == 'Friday'):
        return 5
    if(row['release_day'] == 'Saturday'):
        return 6
    if(row['release_day'] == 'Sunday'):
        return 7


def generate_class_label_certificate(row):
    if(row['certificate'] == 'R'):
        return 1
    if(row['certificate'] == 'G'):
        return 2
    if(row['certificate'] == 'PG'):
        return 3
    if(row['certificate'] == 'PG-13'):
        return 4
    if(row['certificate'] == 'NC-17'):
        return 5
    if(row['certificate'] == 'Approved'):
        return 6
    if(row['certificate'] == 'Not Rated'):
        return 7
    if(row['certificate'] == 'Unrated'):
        return 8
    if(row['certificate'] == 'TV-PG'):
        return 9
    if(row['certificate'] == 'TV-MA'):
        return 7


if __name__ == "__main__":
    data = pd.read_csv('toy_data.csv', encoding='utf-8')

    # Proprocessing has been done on final_imdb.csv in preprocess_main.py for 5389 records
    # data = Preprocess.pre_process(data)

    lr_prep_data = data.copy()
    set_datatype(data)
    set_categorical_type(data)
    # Splitting the dataset
    result = np.random.rand(len(data)) < 0.8
    train, test = data[result].copy(), data[~result].copy()
    actual_labels = []
    for index, row in test.iterrows():
        actual = row['result']
        actual_labels.append(actual)

    # Naive Bayes classification
    X = data.iloc[:, [0, 2, 4, 6, 7, 8, 9, 10, 12, 13, 14,
                      15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]].values
    y = data.iloc[:, 5].values
    X = X.astype(float)
    fs = FeatureScaling(X, y)
    X = fs.fit_transform_X()
    X_train = X[0:train.shape[0], :]
    y_train = y[0:train.shape[0]]
    X_test = X[train.shape[0]:, :]
    y_test = y[train.shape[0]:]
    nb = NaiveBAlg()
    nb.fit(X_train, y_train)
    nb_ypred = nb.predict(X_test)

    eval_nb = Evaluation.evaluate(actual_labels, nb_ypred)
    print('\nNaive Bayes Evaluation')
    print("Accuracy: ", eval_nb['accuracy'])

    lr_prep_data['day'] = lr_prep_data.apply(
        lambda row: generate_class_label(row), axis=1)
    lr_prep_data['certify'] = lr_prep_data.apply(
        lambda row: generate_class_label_certificate(row), axis=1)
    lr_prep_data.drop(['certificate', 'release_day'], axis=1, inplace=True)

    lr_label = lr_prep_data['result']
    lr_train = lr_prep_data.drop('result', axis=1)

    x_train, x_test, y_train, y_test = train_test_split(
        lr_train, lr_label, test_size=0.8, random_state=42)
    x_train = x_train.to_numpy()
    y_train = y_train.to_numpy()
    x_test = x_test.to_numpy()
    y_test = y_test.to_numpy()

    #LogisticRegression
    model = LogisticRegression(learning_rate=0.01, number_of_iterations=100000)
    model.train(x_train, y_train)
    lp_y_pred = model.predict(x_test, 0.5)
    lr_eval = Evaluation.evaluate(y_test, lp_y_pred)
    print('\nLogistic Regression Evaluation')
    print("Accuracy: ", lr_eval['accuracy'])
