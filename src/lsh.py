import numpy as np
from load_data import load_numpy_preprocessed_data, load_metadata, tuning_tree

#Main class for Locality-Sensitive Hashing structure
class LSH:
    #Constructor (hashTables = # of hash tables, numPlanes = # of hyperplanes per hash table)
    def __init__(self, hashTables: int = 10, numPlanes: int = 16):
        self._hashTables = hashTables
        self._numPlanes = numPlanes

        #dataSet = numpy matrix of game vectors
        #shape = (numSamples, dim)
        self._dataSet = None

        #hyperplanes = numpy array of random hyperplane vectors 
        #shape = (_hashTables, _numPlanes, dim), 
        self._hyperplanes = None

        #tables (hashTables) = list of dictionaries with length of _hashTables
        #shape = list(dict[int, list[int]]) 
        #keys = hash code, values = list of indices from _dataSet
        self._tables = None

#Test/Debug area
if __name__ == "__main__":
    test = load_numpy_preprocessed_data()
    meta = load_metadata()

    print("LSH file wired up")
    print("Matrix shape:", test.shape)
    print("First row norm:", np.linalg.norm(test[0]))
    print("Example game:", meta["0"]["Name"])