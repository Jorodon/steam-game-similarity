from rp_tree import RPTree
import random
import time
import multiprocessing as mp

#Takes in dataset and makes it a global variable (prevents multiple copies being created for each worker process)
def globalDataset(dataset):
    global multiprocessor_dataset
    multiprocessor_dataset = dataset

#Non-class function allows multiprocessing to execute, parallelizes the creation of trees
def createTreeGlobal(args):

    #Creates a tree 
    max_level, min_leaf_size, index = args
    rp_tree = RPTree(multiprocessor_dataset, max_level, min_leaf_size)
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

    #Creates an RP forest by creating many individual RP trees (using multi-processing) (Optional use of MultiProcessing)
    def createForest(self, useMP: bool = True):
        
        if useMP:
            #Creates a list of tasks to be divided up among cores 
            #Consists of function inputs for RPTree createTree()
            multi_task_list = []
            for i in range(self._num_of_trees):
                multi_task_list.append([self._max_level, self._min_leaf_size, i])
            
            #Creates a multiprocessing pool to manage pool of worker processes
            with mp.Pool(initializer=globalDataset, initargs=(self._dataset,)) as pool:
                #Maps the list of tasks to the creareTreeGlobal function, returns list of tree roots
                forest_roots = pool.map(createTreeGlobal, multi_task_list)

            #Turns list of tree roots into list of RPTree objects (setting the root for each)
            for root in forest_roots:
                rp_tree = RPTree(self._dataset, self._max_level, self._min_leaf_size)
                rp_tree._root = root
                self._trees.append(rp_tree)

        #Single process version
        else:
            for i in range(self._num_of_trees):
                rp_tree = RPTree(self._dataset, self._max_level, self._min_leaf_size)
                rp_tree.createTree()
                self._trees.append(rp_tree)

    #Traverses through each tree to find similar data, then takes the k most similar data points.
    def traverseForest(self, query_index, k):  
        #Traverses each tree and adds their leaf data to a set (gets rid of duplicate values)
        '''TO DO - Possibly implement a counter to select games that appear more than once and select k similar games from only those games'''
        unique_games = set()
        for i in range(self._num_of_trees):
            unique_games.update(self._trees[i].traverseTree(query_index))

        #Create empty dictionary and obtain the data for the current game query
        cosine_similarity_dict = {}
        query_data = self._dataset[query_index]

        #Calculate the cosine similarity between the set of games and target game
        for index in unique_games:
            sum = 0
            for j in range(len(self._dataset[0])):
                sum += self._dataset[index][j] * query_data[j]
            #Update dictionary with each game and it's cosine simialrity to target game
            cosine_similarity_dict.update({index: sum})

        #Creates a list of the games using a lambda function to sort them by the dictionary values
        sorted_similarity_list = sorted(cosine_similarity_dict, key = lambda d_key : cosine_similarity_dict.get(d_key), reverse = True)

        #Returns only those k-most-similar games
        return sorted_similarity_list[1:k+1]