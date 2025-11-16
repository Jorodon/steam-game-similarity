import os
import random


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
        self.root = self.splitTree(self._dataset, 0)

    # Recursive method to perform the split at each level of the tree
    # Returns a dictionary containing node info:
    # Main nodes: projection vector, left child, and right child
    # Leaf nodes: data
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
        if ((level != None and level >= self._max_level) or data_index.size() < self._min_leaf_size): 
            return {"leaf_node_data": data_index}

        #Generates a random projection vector
        projection_vector = self.generateRandomProjection(data_index.size())

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
            gauss_vector.append(rand_gauss)
        
        #Returns the random projection vector
        return gauss_vector

        

    # Projects the input data onto the projection vector
    # Returns a single value 
    def applyProjection(self, projectionVector, data):
        print("Temp")

    
