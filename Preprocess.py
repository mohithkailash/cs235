
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import DataVisualization as vs
from collections import Counter


def getDay(row):
    if pd.isna(row['release_date']) == False:
        return row['release_date'].strftime('%A')
    else:
        return np.nan


def getYear(row):
    if pd.isna(row['release_date']) == False:
        return row['release_date'].strftime('%Y')
    else:
        return np.nan


def generate_class_label(row):
    # If revenue if greater than or equal to 2 times the budget assign 'Hit' = 1 or 'Flop' = 0
    if(row['revenue'] >= 2*row['budget']):
        return 1
    else:
        return 0


def encode_genres(data):
    genre_list = list([i for i in data['genres']])
    genre_count = Counter([i for j in genre_list for i in j])
    unique_genres = list(genre_count.keys())

    def encode(row):
        for genre in unique_genres:
            if genre in row['genres']:
                row[genre] = 1
            else:
                row[genre] = 0
        return row

    data = data.apply(encode, axis=1)
    return data


def pre_process(data):

    # Dropping duplicates
    data.drop_duplicates(inplace=True)
    data['release_date'] = pd.to_datetime(
        data['release_date'], infer_datetime_format=True)

    # getting day from release date
    data['release_day'] = data.apply(lambda row: getDay(row), axis=1)
    # getting year from release date
    data['release_year'] = data.apply(lambda row: getYear(row), axis=1)

    # Transforming budget to millions
    data['budget'] = data['budget'].apply(lambda row: row/1000000)
    data['revenue'] = data['revenue'].apply(lambda row: row/1000000)

    # Dropping irrelevant features
    data.drop(['imdb_id', 'name', 'release_date'], axis=1, inplace=True)

    # Taking only english movies into consideration
    data = data[data['language'] == "English"]

    empty_revenue_rows = data[data['revenue'] == 0].shape[0]
    # Ignoring records with "0" revenue
    if empty_revenue_rows > 0:
        data = data[data['revenue'] != 0]

    # Ignoring records with "0" budget
    empty_budget_rows = data[data['budget'] == 0].shape[0]
    if empty_budget_rows > 0:
        data = data[data['budget'] != 0]

    empty_runtime_rows = data[data['runtime'] == 0].shape[0]
    # Replacing missing runtime values with mean
    if empty_runtime_rows > 0:
        data['runtime'] = data['runtime'].replace(0, data['runtime'].mean())

    # Generating class label
    data['result'] = data.apply(lambda row: generate_class_label(row), axis=1)

    # Transforming genres
    data['genres'] = data['genres'].apply(lambda col: col.split(", "))

    # Dropping records with null columns
    cols = ['release_day', 'language']
    data.dropna(subset=cols, how='any', inplace=True)

    # converting release_year to int
    data['release_year'] = data['release_year'].apply(lambda col: int(col))

    # vs.show_correlation_matrix(data)
    # vs.budget_vs_revenue(data)
    # vs.runtime_vs_revenue(data)
    # vs.votes_vs_revenue(data)
    # vs.imdb_rating_vs_revenue(data)
    # vs.metascore_vs_revenue(data)
    # vs.releaseday_vs_revenue(data)
    # vs.genre_distribution(data)

    # One hot encoding for genres
    data = encode_genres(data)

    # Dropping irrelevant features
    cols = ['revenue', 'imdb_rating', 'meta_score',
            'votes', 'genres', 'language']
    data.drop(cols, axis=1, inplace=True)

    return data
