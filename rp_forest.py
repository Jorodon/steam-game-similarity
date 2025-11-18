from rp_tree import RPTree
import random
import time
import multiprocessing as mp

#Non-class function allows multiprocessing to execute, parallelizes the creation of 
def createTreeGlobal(args):

    #Creates a tree 
    dataset, max_level, min_leaf_size, index = args
    rp_tree = RPTree(dataset, max_level, min_leaf_size)
    rp_tree.createTree()

    #Tracks ending time of forest creation and prints result
    print(f"Created tree {index+1}")

    #Returns RPTree object
    return rp_tree._root

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
            forest_roots = pool.map(createTreeGlobal, multi_task_list)

        for root in forest_roots:
            rp_tree = RPTree(self._dataset, self._max_level, self._min_leaf_size)
            rp_tree._root = root
            self._trees.append(rp_tree)

    #Traverses through each tree to find similar data, then takes the k most similar data points.
    def traverseForest(self, query_index, k):  
        similar_games = set()

        for i in range(self._num_of_trees):
            similar_games.update(self._trees[i].traverseTree(query_index))

        print(similar_games)

        return similar_games