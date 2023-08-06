"""
author : Liji Alex
email : liji.alex@gmail.com
"""

import os
import joblib
import pandas as pd
#from utils.model import Perceptron
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import logging
import os
from oneNeuron.perceptron import Perceptron

logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename = os.path.join(log_dir,"running_logs.log"),level=logging.INFO, format=logging_str)


def createModel(data, eta, epoch, file_name, plot_name, no_of_input=2):       
      
    logging.info(f"\n\n>>>>>>>>>>Starting training>>>>>>>>>>>>>>>>{file_name}")
    logging.info(f"eta = {str(eta)} epochs ={str(epoch)}\n")

    df = pd.DataFrame(data)

    X,y = prepare_data(df)
    logging.info(f"X={X}")
    logging.info(f"Y={y}")    

    model = Perceptron(eta, epoch, no_of_input)

    model.fit(X, y)

    model.predict(X)

    model.total_loss()

    save_model(model, file_name)

    
    logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    if no_of_input == 2:
      save_plot(df, plot_name, model)

def prepare_data(df):
  """It is used to seperate dependent variables and independent variables

  Args:
      df (pd.DataFrame): its the pandas DataFrame

  Returns:
      tuple: it returns the tuples of dependent variables and independent variables
  """
  X = df.drop("y",axis=1)

  y=df["y"]

  return X, y

def save_model(model, filename):
  """This saves the trained model

  Args:
      model (Python Object): Trained Model
      filename (str): path to save the trained model
  """
  model_dir = "models"
  os.makedirs(model_dir,exist_ok=True) #create only if model directory dosent exists
  filePath = os.path.join(model_dir, filename)
  logging.info(filePath)
  joblib.dump(model, filePath)

def save_plot(df, file_name, model):
  """[saves the plot]

  Args:
      df ([pandas df]): [its a dataframe]
      file_name ([string]): [its path to save the plot]
      model ([model object]): [trained model]
  """

  def _create_base_plot(df):
    #plot scatter plot of df 
    
    df.plot(kind="scatter", x="x1", y="x2", c="y", s=100, cmap="winter")
    #draw h and v line
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8) #set size of the graph
  
  def _plot_decision_regions(X, y, classfier, resolution=0.02):
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])  #select colours for unique y

    X = X.values # take x as a array
    x1 = X[:, 0]  #get first column    
    x2 = X[:, 1]  #get second column
    #print(f"X = \n{X}")
    #print(f"x1 = {x1}")
    #print(f"x2 = {x2}")
    #get min values for plotting
    #-1,+1 done for getting a wider area ie -1 to +2
    x1_min, x1_max = x1.min() -1 , x1.max() + 1
    x2_min, x2_max = x2.min() -1 , x2.max() + 1  

    #get inbetween points from -1 to +2
    
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), 
                          np.arange(x2_min, x2_max, resolution))
    #change to a flattened array and predict
    Z = classfier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    #reshape to original array
    Z = Z.reshape(xx1.shape)
    #plot graph
    plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    plt.plot()
    
    #print(f"xx1 = \n{xx1}")
    #print(f"xx2 = \n{xx2}")

    #print(f"xx1.ravel() = \n{xx1.ravel()}")
    #print(f"xx2.ravel() = \n{xx2.ravel()}")
    
    
    

  X, y = prepare_data(df)
  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  plotPath = os.path.join(plot_dir, file_name) # model/filename
  plt.savefig(plotPath)