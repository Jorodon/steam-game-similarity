import os
import random
import numpy as np
import json
import load_data_test
import sys
import statistics

#sys.setrecursionlimit(10000)
#random.seed(50)

class RPTree:
    #Class for a single Random Projection Tree
    #Instance variables:
        #dataset - the entire raw dataset for tree
        #min_leaf_size - the minimum number of elements in a node to justify splitting (default is 1)
        #max_level - the maximum level of the tree 
        #root - the root node of the tree (initialized to None)

    def __init__(self, dataset, max_level=None, min_leaf_size=1):
        self._dataset = dataset
        self._min_leaf_size = min_leaf_size
        self._max_level = max_level
        self._root = None

    # Starts the process of creating a RP Tree
    # Returns nothing
    def createTree(self):
        data_index = [index for index in range(len(self._dataset))]
        self._root = self.splitTree(data_index, 0)

    # Recursive method to perform the split at each level of the tree
    # Returns a RPTreeNode object containing node info
    def splitTree(self, data_index, level):
        '''
        # if level exists and level is > max level and size of data < min_leaf_size:
            # Return dictionary {data}
        
        # Steps for recursive case:
            # Generate random projection vector
            # Project data onto vector
            # Find the split point (median?)
            # Split the tree based on split point
            # Recursively call L and R child
            # Return dictionary {projection vector, left child, right child}
        '''

        #Checks base case (where max level has been reached) and returns dictionary for leaf node
        if ((self._max_level != None and level >= self._max_level) or len(data_index) < self._min_leaf_size): 
            return RPTreeNode(data_index)

        max_retries = 10

        for retry in range(max_retries):
                
            #Generates a random projection vector
            projection_vector = self.generateRandomProjection(len(self._dataset[0]))

            #Projects data onto projection vector
            projected_data = self.applyProjection(projection_vector, data_index)

            #Calculates median of projection vector
            median = statistics.median(projected_data.values())     

            #Splits the tree into left/right subtrees based on median
            left_values = [index for index in data_index if projected_data[index] < median]
            right_values = [index for index in data_index if projected_data[index] >= median]

            if len(left_values) > 0 or len(right_values) > 0:
                break

        if len(left_values) == 0 or len(right_values) == 0:
            # print(f"error{level}")
            # print("Left values:\n")
            # for i in range(len(left_values)):
            #     print(self._dataset[i][:])
            #     print(projected_data[left_values[i]])
            #     print('\n')
            # print("Right values:\n")
            # for i in range(len(right_values)):
            #     print(self._dataset[i][:])
            #     print(projected_data[right_values[i]])
            #     print('\n')
            # print(projection_vector)
            return RPTreeNode(data_index)
        #Recursively split tree for left and right child
        left_child = self.splitTree(left_values, level + 1)
        right_child = self.splitTree(right_values, level + 1)

        #Returns a RPTreeNode() object containing node data
        return RPTreeNode(None, projection_vector, median, left_child, right_child)

    # Generates a random projection vector with the same number of dimensions as the dataset
    # Returns a vector
    def generateRandomProjection(self, dimension):
        #Determines the row and column size for a random gaussian matrix, initializes empty lsit
        col_D = dimension
        gauss_vector = []

        #Iterates through each column in the 1D array, generating a random number from a gaussian distribution
        for j in range(col_D):
            #Mean chosen as 0 and standard deviation chosen as 1
            rand_gauss = random.gauss(0, 1)
            temp_vector = [rand_gauss]
            gauss_vector.append(temp_vector)
        
        #Returns the random projection vector
        return gauss_vector

    # Projects the input data onto the projection vector
    # Returns a dictionary of projected values
    def applyProjection(self, projection_vector, data_index):
        #Create empty dictionary
        projected_data = {}

        #Perform the dot product of the projection vector and each row of data within the node's data matrix
        for index in data_index:
            sum = 0
            for j in range(len(self._dataset[0])):
                sum += self._dataset[index][j] * projection_vector[j][0]
            projected_data.update({index: sum})

        #Returns the projected_data matrix
        return projected_data
    
    #Traverses the RPTree to find similar games (ones in the same leaf node)
    def traverseTree(self, query_index):
        #Determines the data to be used in query from index input
        query_data = self._dataset[query_index]

        #Calls traverseNodes() from RPTreeNode to recursively find and return the indices of similar data
        return RPTreeNode.traverseNodes(self._root, query_data)
    
    #Test method for viewing the RPTree dictionary representation
    def outputDictDebug(self):

        '''#Added a json file output for tree data to help visualization
        dir = "resources"
        subfolder = "preprocessed_data"
        sub_path = os.path.join(dir, subfolder)
        dict_data_path = os.path.join(sub_path, "rp_tree_dictionary.json")
        with open(dict_data_path, 'w') as file:
            json.dump(self._root, file, indent=5)'''

        return

class RPTreeNode():
    #Class to hold data for a single RPTree Node
    #Instance variables:
        #Leaf nodes: 
            #data_index - list of indexes that are grouped under the same leaf node
        #Inner ndoes:
            #projection_vector - the projection vector used to decide the split for the current node
            #median - the median value recorded for the projections of each node
            #left_child - a RPTreeNode object containing data for the left child node
            #right_child - a RPTreeNode object containing data for the lrightchild node

    def __init__(self, data_index=None, projection_vector=None, median=None, left_child=None, right_child=None):
        self._data_index = data_index
        self._projection_vector = projection_vector
        self._median = median
        self._left_child = left_child
        self._right_child = right_child

    #Traverses through each node in the tree
    def traverseNodes(self, query_data):
        #Base case: returns an array containing all the indexes in a leaf node when one is reached
        if self._data_index != None:
            return self._data_index
        
        #Calculates the projection of the query vector 
        query_dot = 0
        for index in range(len(self._projection_vector)):
            query_dot += query_data[index] * self._projection_vector[index][0]

        #Determines which child node to recursively call based on where the projection falls around median
        if query_dot < self._median:
            return self._left_child.traverseNodes(query_data)
        else:
            return self._right_child.traverseNodes(query_data)