import numpy as np
import os
import json

#Test function to load preprocessed data matrix
def load_preprocessed_data():
    #Creates an input path for the preprocessed_data
    dir = "resources"
    subfolder = "preprocessed_data"
    sub_path = os.path.join(dir, subfolder)
    matrix_data_path = os.path.join(sub_path, "preprocessed_data_matrix.npy")

    #Loads the data and converts it to a python array
    numpy_matrix = np.load(matrix_data_path)
    converted_matrix = numpy_matrix.tolist()
    
    #Returns the python array containing preprocessed data
    return converted_matrix

'''def load_metadata():
    dir = "resources"
    subfolder = "preprocessed_data"
    sub_path = os.path.join(dir, subfolder)
    metadata_data_path = os.path.join(sub_path, "preprocessed_data_matrix.npy")
    return'''
