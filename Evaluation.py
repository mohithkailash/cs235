import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score


def evaluate(y_actual, y_pred):
    accuracy = accuracy_score(y_actual, y_pred)
    precision = precision_score(y_actual, y_pred)
    recall = recall_score(y_actual, y_pred)
    f1score = f1_score(y_actual, y_pred)

    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1score": f1score}
