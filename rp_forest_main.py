import os
import random
import numpy as np

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
        data_index = [index for index in self._dataset]
        self.root = self.splitTree(data_index, 0)

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
        projection_vector = self.generateRandomProjection(data_index[0].size())

        #Projects data onto projection vector
        projected_data = self.applyProjection(projection_vector)

        #Calculates median of projection vector
        sum = sum(projected_data)
        median = sum / projected_data.size()

        #Splits the tree into left/right subtrees based on median
        left_values = [index for index in data_index if projected_data[index] < median]
        right_values = [index for index in data_index if projected_data[index] >= median]

        #Recursively split tree for left and right child
        left_child = self.splitTree(left_values, level + 1)
        right_child = self.splitTree(right_values, level + 1)

        #Returns a dictionary (multi-dimensional) containing node data
        return {
            "projection_vector": projection_vector,
            "left_child": left_child,
            "right_child": right_child
        }

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
    # Returns a dictionary of projected values
    def applyProjection(self, projection_vector, data_index):
        #Create empty dictionary
        projected_data = {}

        #Perform the dot product of the projection vector and each row of data within the node's data matrix
        for index in data_index:
            sum = 0
            for j in range(projection_vector.size()):
                sum += projection_vector[j] * self._dataset[index][j]
            projected_data.update(index, sum)

        #Returns the projected_data matrix
        return projected_data
    
    #Test method for printing the RPTree dictionary representation
    def printDebug(self):
        for key,value in self._root:
            print(key, value)

        return


#Test main method
def main():

    #Loads preprocessed data and creates an RPTree using it
    initial_data = load_preprocessed_data()
    rp_tree = RPTree(initial_data, 10, 20)
    rp_tree.createTree()

    #Tests if tree creation works properly
    rp_tree.printDebug()


if __name__ == "__main__":
    main()