""" 
Author: Karthik Arumugam
Email: karthik131100@gmail.com
"""

import numpy as np
import logging 
from tqdm import tqdm  

class Perceptron:
  def __init__(self, eta,epochs):
    # np.random.seed(42) - If we want the same weights of random values any where in the method
    self.weights = np.random.randn(3) * 1e-4 # 1e-4 To make Small weight initialization, 3 weights as we have 3 weights w1,w2,w0
    logging.info(f"initial weights before training: \n{self.weights}")
    self.eta = eta # learning rate
    self.epochs = epochs # No of epochs

  def activationFunction(self, inputs, weights):
    z = np.dot(inputs, weights)  # Z = w1.x1 + w2.x2 +..../ W*X
    return np.where(z > 0,1,0)   # Condition:- return z=1 if z>0 & z=0 if z<0

  def fit(self, X, y):
    self.X = X
    self.y = y

    X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))] # Concatenating -1 bias matrix with X data using np.c_
    logging.info(f"X with bias: \n{X_with_bias}")

    for epoch in tqdm(range(self.epochs), total=self.epochs, desc="Training the model"):
      logging.info("--"*10)
      logging.info(f"for epoch: {epoch}")

      y_hat = self.activationFunction(X_with_bias, self.weights) # Predicting the y - Forward propagation
      logging.info(f"predicted value after forward pass: \n{y_hat}")

      self.error = self.y - y_hat  # Calculating the error
      logging.info(f"error: \n{self.error}")

      self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error) # Updating the weights- Back Propagation
      logging.info(f"updated weights after epoch: \n{epoch}/{self.epochs}: \n {self.weights}")
      logging.info("#####"*10)
 
  def predict(self, X):
    X_with_bias = np.c_[X, -np.ones((len(X), 1))]
    return self.activationFunction(X_with_bias, self.weights)

  def total_loss(self):
    total_loss = np.sum(self.error)
    logging.info(f"total loss: {total_loss}")
    return total_loss