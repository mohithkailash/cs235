import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

sns.set(color_codes=True)


def show_correlation_matrix(data):
    correlation = data.corr()
    plt.figure(figsize=(10, 10))
    sns.heatmap(correlation, square=True, annot=True)
    plt.show()


def budget_vs_revenue(data):
    ax = sns.scatterplot(x="budget", y="revenue", data=data)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Budget")
    plt.show()


def runtime_vs_revenue(data):
    ax = sns.scatterplot(x="runtime", y="revenue", data=data)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Runtime")
    plt.show()


def imdb_rating_vs_revenue(data):
    ax = sns.scatterplot(x="imdb_rating", y="revenue", data=data)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("IMDB Rating")
    plt.show()


def votes_vs_revenue(data):
    ax = sns.scatterplot(x="votes", y="revenue", data=data)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("User Votes")
    plt.show()


def metascore_vs_revenue(data):
    ax = sns.scatterplot(x="meta_score", y="revenue", data=data)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Metascore")
    plt.show()


def genre_distribution(data):
    genre_list = list([i for i in data['genres']])
    genre_count = Counter([i for j in genre_list for i in j])
    labels, values = zip(*Counter(genre_count).items())
    indexes = np.arange(len(labels))

    plt.figure(figsize=(25, 8))
    plt.bar(indexes, values)
    plt.xticks(indexes, labels)
    plt.xlabel('Genre')
    plt.ylabel('Frequency')
    plt.title('Genre Distribution')
    plt.savefig('genre vs count.jpg')
    plt.show()


def releaseday_vs_revenue(data):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="release_day", y="revenue", data=data, ci=None)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("Release Date")
    plt.show()
