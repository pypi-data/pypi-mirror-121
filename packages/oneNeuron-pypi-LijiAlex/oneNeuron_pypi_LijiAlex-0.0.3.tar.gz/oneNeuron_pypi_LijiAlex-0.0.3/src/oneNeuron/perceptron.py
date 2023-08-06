import numpy as np
import logging
import os
from tqdm import tqdm

logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename = os.path.join(log_dir,"running_logs.log"),level=logging.INFO, format=logging_str)


class Perceptron:
  def __init__(self,eta,epochs,no_of_input):
    self.weights = np.random.randn(no_of_input+1) *1e-4 #small weight initialization
    logging.info(f"initial weights before training: {self.weights}")
    self.eta = eta #learning rate
    self.epochs = epochs #no of epochs
  
  def activationFunction(self,inputs,weights):
    z = np.dot(inputs, weights) # z = X * W  
    return np.where(z > 0, 1, 0) # if >0 return 1 else 0

  def fit(self,X,y):  #training
    self.X = X
    self.y = y

    x_with_bias = np.c_[X, -np.ones((len(X),1))] #len is no of rows of X np.c_ is concatinaete
    logging.info(f"X with bias: \n{x_with_bias}")

    for epoch in tqdm(range(self.epochs), total = self.epochs, desc = "training the model"):
      logging.info("__"*10)
      logging.info(f"for epoch:{epoch}")
      logging.info("__"*10)

      y_hat = self.activationFunction(x_with_bias,self.weights) #forward propagation
      logging.info(f"predicted value after forward pass: \n{y_hat}")
      self.error = self.y - y_hat
      logging.info(f"error: \n{self.error}")
      self.weights = self.weights + self.eta * np.dot(x_with_bias.T,self.error) #backward propagation
      logging.info(f"corrected weights after epoch:{epoch}/{self.epochs} :{self.weights} ")
      logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
      
  def predict(self,X):
    x_with_bias = np.c_[X, -np.ones((len(X), 1))]
    return self.activationFunction(x_with_bias,self.weights)

  def total_loss(self):
    total_loss = np.sum(self.error)
    logging.info(f"Total loss : {total_loss}")

    if total_loss == 0:
      msg = "MODEL CREATION SUCCESSFUL"
    else:
      msg = "MODEL CREATION FAILED, Try with different, epochs, learning rate or a different approach altogether"
    logging.info(msg)

    logging.info(f"total loss = {str(total_loss)}\n")
    logging.info(msg+"\n")
    
    return total_loss