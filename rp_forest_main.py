import os


class RPTree:
    #Class for a single Random Projection Tree
    #Instance variables:
        #dataset - the entire raw dataset for tree
        #min_leaf_size - the minimum number of elements required to be in a leaf node (default is 1)
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
        print("temp")

    # Recursive method to perform the split at each level of the tree
    # Returns vector containing projection vector, left child, and right child
    def splitTree(self, data, height):
        print("temp")

    # Generates a random projection vector with the same number of dimensions as the dataset
    # Returns a vector
    def generateRandomProjection(self, dimension):
        print("temp")

    # Projects the input data onto the projection vector
    # Returns a single value 
    def applyProjection(self, projectionVector, data):
        print("Temp")

    
