from rp_tree import RPTree
import random
import time



class RPForest:
    #Class for a Random Projection Forest
    #Instance variables:
        #dataset - the entire raw dataset for tree
        #num_of_trees - the number of trees to be built using the dataset
        #min_leaf_size - the minimum number of elements in a node to justify splitting (default is 1)
        #max_level - the maximum level of the tree 
        #trees - list storing individual RPTree objects

    def __init__(self, dataset, num_of_trees, max_level=None, min_leaf_size=1):
        self._dataset = dataset
        self._num_of_trees = num_of_trees
        self._min_leaf_size = min_leaf_size
        self._max_level = max_level
        self._trees = []

    def createForest(self):
        
        

        #Creates the desired number of trees and appends them to list _trees
        for i in range(self._num_of_trees):
            #Tracks start of tree creation time
            tree_create_start = time.time()

            rp_tree = RPTree(self._dataset, self._max_level, self._min_leaf_size)
            rp_tree.createTree()
            self._trees.append(rp_tree)

            #Tracks end of tree creation time and prints time taken
            tree_create_end = time.time()
            time_passed = tree_create_end - tree_create_start
            print(f"Time to create tree {i+1} is {time_passed}")

        # test_index = random.randint(0, 111452)
        # data_indices = rp_tree.traverseTree(test_index)
        # print(f"Test Index: {test_index}\nData Indices: {data_indices}")

    def traverseForest(self):  
        print("temp")