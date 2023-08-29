#!/usr/bin/env python3

import rospy
import os
import bagpy
import pandas as pd
import numpy as np
from bagpy import bagreader
from os import listdir
from os.path import isfile, join
from numpy import genfromtxt

ROSBAG_FILE_DIR = "/home/vboxuser/MMP/catkin_ws/src/rosbag_files/"
ROSBAG_TOPICS = ["/infrareds", "/cmd_vel"]

INFRAREDS_NUMPY_FILE_PATH = "/home/vboxuser/MMP/numpy_arrays/infrareds/"
CMD_VEL_NUMPY_FILE_PATH = "/home/vboxuser/MMP/numpy_arrays/cmd_vel/"

INFRAREDS_CSV_FINAL_PATH = "/home/vboxuser/MMP/catkin_ws/src/rosbag_files/final_csvs/combined_infrareds.csv"
CMD_VEL_CSV_FINAL_PATH = "/home/vboxuser/MMP/catkin_ws/src/rosbag_files/final_csvs/combined_cmd_vel.csv"

INFRAREDS_COLUMNS = [10,19,28,37,46,55,64]
CMD_VEL_COLUMNS = [2,7]

#Create a list of files from the directory (and not the sub-directories created by bagreaders)
files = [file for file in listdir(ROSBAG_FILE_DIR) if (isfile(join(ROSBAG_FILE_DIR, file)) and file.endswith('.bag'))] 

#Store each csv file into a list
infrareds_csvs = []
cmd_vel_csvs = [] 

#Store the numpy arrays created by reading each csv file into a list
infrareds_np_array_list = []
cmd_vel_np_array_list = [] 

for file in files:
    #Read each bag file and create a csv file for each topic within it
    bag_reader = bagreader(join(ROSBAG_FILE_DIR, file))
    for topic in ROSBAG_TOPICS:
        csv = bag_reader.message_by_topic(topic)
        read_csv = pd.read_csv(csv)
        read_csv.dropna()

        #Check to see which csv we are looking at, store it in the appropriate list
        if ROSBAG_TOPICS[0] in csv:
            infrareds_csvs.append(read_csv)
        elif ROSBAG_TOPICS[1] in csv:
            cmd_vel_csvs.append(read_csv)

#Use pandas to concatenate the csvs into one large dataframe each
combined_infrareds_csvs = pd.concat(infrareds_csvs)
combined_cmd_vel_csvs = pd.concat(cmd_vel_csvs)

#Save the dataframes as a csv file
combined_infrareds_csvs.to_csv(INFRAREDS_CSV_FINAL_PATH, delimiter=',')
combined_cmd_vel_csvs.to_csv(CMD_VEL_CSV_FINAL_PATH, delimiter=',')

#Create a numpy array from the new concatenated csv 
infrareds_np_array = genfromtxt(INFRAREDS_CSV_FINAL_PATH, delimiter=',')
cmd_vel_np_array = genfromtxt(CMD_VEL_CSV_FINAL_PATH, delimiter=',')

#Extract the columns we are interested in from the numpy array
infrareds_np_array = infrareds_np_array[:,INFRAREDS_COLUMNS]
cmd_vel_np_array = cmd_vel_np_array[:,CMD_VEL_COLUMNS]

#Remove NaN values
infrareds_np_array = infrareds_np_array[~np.isnan(infrareds_np_array).any(axis=1)]
cmd_vel_np_array = cmd_vel_np_array[~np.isnan(cmd_vel_np_array).any(axis=1)]

#Save the numpy arrays
np.save(INFRAREDS_NUMPY_FILE_PATH + "infrareds_numpy", infrareds_np_array)
np.save(CMD_VEL_NUMPY_FILE_PATH + "cmd_vel_numpy", cmd_vel_np_array)
