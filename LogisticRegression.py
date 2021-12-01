import numpy as np


class LogisticRegression:
    # constructor to initialization of learning_rate and number_of_iterations
    def __init__(self, learning_rate=0.01, number_of_iterations=100000, intercept=True):
        self.learning_rate = learning_rate
        self.number_of_iterations = number_of_iterations
        self.intercept = intercept

    # method for adding theta0
    def __add_intercept(self, X):
        intercept = np.ones((X.shape[0], 1))
        return np.concatenate((intercept, X), axis=1)

    # Sigmoid function or Logarithmic function

    def __sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    # Loss function which is used in logistic regression to(give penality to wrong decisions)
    # h-> hypothesis function
    def __loss(self, h, y):
        return (-y * np.log(h) - (1 - y) * np.log(1 - h)).mean()
    # The function which is used to train the classifier from the given train data

    def train(self, X, y):
        if self.intercept:
            X = self.__add_intercept(X)
        # theta initialization
        self.theta = np.zeros(X.shape[1])
        for i in range(self.number_of_iterations):
            z = np.dot(X, self.theta)
            h = self.__sigmoid(z)
            # calculating gradient descent from loss function
            gradient = np.dot(X.T, (h - y)) / y.size
            self.theta -= self.learning_rate * gradient  # updating the theta values

    def predict_prob(self, X):
        if self.intercept:
            X = self.__add_intercept(X)
        return self.__sigmoid(np.dot(X, self.theta))

    # Function to predict the output for the training data
    def predict(self, X, threshold):
        return self.predict_prob(X) >= threshold
