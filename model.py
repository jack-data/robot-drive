import rospy
import os
import pandas as pd
import numpy as np
import sys
import joblib

from datetime import datetime
from tkinter import *
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
from numpy import genfromtxt
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression

#Open the infrareds and cmd_vel numpy files using tkinter GUI
Tk().withdraw()
infrareds_numpy_file = filedialog.askopenfilenames(initialdir="", title="Select the infrareds numpy file")

Tk().withdraw()
cmd_vel_numpy_file = filedialog.askopenfilenames(initialdir="", title="Select the cmd_vel numpy file")

if (len(infrareds_numpy_file) <= 0) or (len(cmd_vel_numpy_file) <= 0):
    print("No file was selected. Exiting...")

if (len(infrareds_numpy_file) > 1) or (len(cmd_vel_numpy_file) > 1):
    print("Please only select one file for each type. Exiting...")

#Convert type to string so that they may be opened with np.load()
#Filedialog returns a tuple so needs to access first index with [0] syntax
infrareds_numpy_file = str(infrareds_numpy_file[0])
cmd_vel_numpy_file = str(cmd_vel_numpy_file[0])

infrareds_np_array = np.load(infrareds_numpy_file)
cmd_vel_np_array = np.load(cmd_vel_numpy_file)

#Take a percentage of the data to use as training data
number_of_instances = infrareds_np_array.shape[0]
training_percentage = 0.8
training_percentage = int(number_of_instances * training_percentage)

#Split the data into the above percentage for training and testing data
infrareds_train, cmd_vel_train = infrareds_np_array[:training_percentage], cmd_vel_np_array[:training_percentage]
infrareds_test, cmd_vel_test = infrareds_np_array[training_percentage:], cmd_vel_np_array[training_percentage:]

#Create a model on training data
#3 models which work for outputting 2 values: RandomForestRegressor, KNeighborsRegressor, LinearRegression
#Simple cmd line interface for choosing which model to run
while True:
    model_choice = input("""
    Please select a model to train:\n
    1. Random Forest
    2. K Neighbours
    3. Linear Regression
    """)
    if model_choice == "1":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model_name = "RandForest"
        break
    elif model_choice == "2":
        model = KNeighborsRegressor(n_neighbors=2)
        model_name = "KNeigh"
        break
    elif model_choice == "3":
        model = LinearRegression()
        model_name = "LinReg"
        break
    else:
        print("Please only enter 1, 2 or 3 as input.")

model.fit(infrareds_train, cmd_vel_train)

#Save the model so it can be opened and used elsewhere
model_name = f"{model_name} {datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}"
joblib.dump(model, f"{model_name}.pkl")
print(f"Model saved as {model_name}.pkl")