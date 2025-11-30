import numpy as np
import os
import json
import time

from sklearn.neighbors import NearestNeighbors

'''Uses scikit to perform a brute force comparison of all games to input game and find the k-most-similar'''
def tuning_tree(game_index, k):
    #Creates an input path for the preprocessed_data
    dir = "resources"
    subfolder = "preprocessed_data"
    sub_path = os.path.join(dir, subfolder)
    matrix_data_path = os.path.join(sub_path, "preprocessed_data_matrix.npy")

    #Loads the data into 2d numpy array
    numpy_matrix = np.load(matrix_data_path)
    brute_force_start = time.time()
    #Creates and fits a brute force nearest neighbor search to the input matrix
    neighbor_brute = NearestNeighbors(n_neighbors=k+1, algorithm='brute', metric='cosine').fit(numpy_matrix)
    
    #Returns a matrix containing the k-nearest-neighbors and converts it to a python list
    nearest_neighbors = neighbor_brute.kneighbors([numpy_matrix[game_index, :]], k+1, False)

    brute_force_end = time.time()
    time_passed = brute_force_end - brute_force_start
    print(f"Time to run brute force is {time_passed}")

    nn_list = nearest_neighbors.tolist()
    return nn_list[0][1:]


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

#Function to load preprocessed data matrix
def load_numpy_preprocessed_data():
    #Creates an input path for the preprocessed_data
    dir = "resources"
    subfolder = "preprocessed_data"
    sub_path = os.path.join(dir, subfolder)
    matrix_data_path = os.path.join(sub_path, "preprocessed_data_matrix.npy")

    #Loads the data into a numpy array
    numpy_matrix = np.load(matrix_data_path)
    
    #Returns the numpy array
    return numpy_matrix

def load_metadata():
    #Creates an input path for the preprocessed_data
    dir = "resources"
    subfolder = "preprocessed_data"
    sub_path = os.path.join(dir, subfolder)
    metadata_path = os.path.join(sub_path, "game_metadata.json")

    #Loads the data and converts it to a python array
    with open(metadata_path, 'r') as file:
            metadata = json.load(file)
    
    #Returns the python array containing preprocessed data
    return metadata