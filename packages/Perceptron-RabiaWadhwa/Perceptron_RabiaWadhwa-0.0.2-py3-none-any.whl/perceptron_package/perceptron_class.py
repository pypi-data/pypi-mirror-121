import numpy as np
import pandas as pd
import logging 
from tqdm import tqdm

# No need to define the Logging Configuration here

class Perceptron:
  def __init__(self,eta,epochs):  #initialise object
    self.weights = np.random.randn(3) *1e-4 # Returns an array of length 3 with random values from standard normal distribution
    #self.weights = np.reshape(self.weights, (3,1))  # 3 rows,1 column
    logging.info(f"Shape of Weights {self.weights.shape}")
    # Example : array([ 3.83262836e-05,  8.66627761e-05, -2.10441382e-04]) ,  multiply by 0.0001 to get even smaller values

    logging.info(f"initial Weights before Training \n{self.weights}")
    self.eta = eta
    self.epochs = epochs
  

  def activation_fn(self,inputs,weights):
    z = np.dot(inputs ,weights) # summation of wi * xi ,here we use function args and not the object variables
    logging.info(f"Dot Product Of Input * Weights \n{z}")
    step_fn = np.where(z>0,1,0)
    logging.info(f"Apply Step function \n{step_fn}")
    return step_fn

  def fit(self,X,y):
    self.X = X
    self.y = y

    X_with_bias = np.c_[self.X,-np.ones((len(self.X) ,1 ))]  # Append x0 to x1 and x2
    ''' #Note: 2 brackets necessary for (Row,Column) interpretation
    > -np.ones((4,1))  #4 rows,1 col
     array([[-1.],
       [-1.],
       [-1.],
       [-1.]]) '''

    for epoch in tqdm( range(self.epochs), total= self.epochs , desc= "training model epochs"):
      logging.info("\n")
      logging.info("-"*20)
      logging.info(f"Epoch {epoch}")

      # Forward Propagation
      y_hat = self.activation_fn(X_with_bias , self.weights) # Calculate Y= activation_fn(summation of wixi)
      logging.info(f"\nPredicted Value : \n{y_hat}")
      
      self.error = self.y - y_hat  # Actual Y - Predicted Y
      logging.info(f"\nError: \n{self.error}")
      
      # Backward Propagation
      self.weights = self.weights + self.eta * (np.dot(X_with_bias.T,self.error)) #x_with_bias transpose * error

      logging.info(f"\nEpoch {epoch}/{self.epochs} \nUpdated Weights : {self.weights}")
      logging.info("-"*20)

  def predict(self,X):
      X_with_bias = np.c_[X,-np.ones((len(X),1))]
      return self.activation_fn(X_with_bias , self.weights)  #This objects's activation fn

  def total_loss(self):
      loss = np.sum(self.error)  #self.error => This object's Error
      logging.info(f"Total Error : {loss}")
      return loss