from rp_tree import RPTree
import random
import time
import multiprocessing as mp

#Non-class function allows multiprocessing to execute, parallelizes the creation of 
def createTreeGlobal(dataset, max_level, min_leaf_size, tree_index):
    #Tracks time to create a tree
    tree_create_start = time.time()

    #Creates a tree 
    rp_tree = RPTree(dataset, max_level, min_leaf_size)
    rp_tree.createTree()

    #Tracks ending time of forest creation and prints result
    tree_create_end = time.time()
    time_passed = tree_create_end - tree_create_start
    print(f"Time to create tree {tree_index} is {time_passed}")

    #Returns RPTree object
    return rp_tree

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

    #Creates an RP forest by creating many individual RP trees
    def createForest(self):
        
        multi_task_list = []
        for i in range(self._num_of_trees):
            multi_task_list.append([self._dataset, self._max_level, self._min_leaf_size, i])
        
        with mp.Pool() as pool:
            self._trees = pool.map(createTreeGlobal, multi_task_list)

    def traverseForest(self):  
        print("temp")