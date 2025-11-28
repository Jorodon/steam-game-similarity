import numpy as np
from load_data import load_numpy_preprocessed_data, load_metadata, tuning_tree
import time

#Main class for Locality-Sensitive Hashing structure
class LSH:
    #Constructor (hashTables = # of hash tables, numPlanes = # of hyperplanes per hash table)
    def __init__(self, hashTables: int = 10, numPlanes: int = 16):
        self._hashTables = hashTables
        self._numPlanes = numPlanes

        #dataSet = numpy matrix of game vectors
        #shape = (numSamples, dim)
        self._dataSet = None

        #hyperplanes = 3D numpy array of random hyperplane vectors 
        #shape = (_hashTables, _numPlanes, dim), 
        self._hyperplanes = None

        #tables (hashTables) = list of dictionaries with length of _hashTables
        #type = list(dict[tuple, list[int]]) 
        #keys = tuple hash code, values = list of indices from _dataSet
        self._tables = None



    #Function that checks if LSH is built
    def isBuilt(self) -> bool:
        if self._dataSet is None or self._hyperplanes is None or self._tables is None:
            return False
        return True
    


    #Function that builds LSH tables from normalized dataset
    def build(self, dataSet: np.ndarray) -> None:
        
        #grabs number of entries and the vector dimension from the dataset shape
        numGames = dataSet.shape[0]
        dims = dataSet.shape[1]

        #Sets class variable _dataSet to called dataset
        self._dataSet = dataSet

        #Creates 3D numpy array of floats -> _hyperplanes[table][hyperplane in table][floats for given hyperplane]
        self._hyperplanes = np.random.normal(size = (self._hashTables, self._numPlanes, dims))

        #Creates an empty list of dictionaries for each table
        self._tables = [dict() for t in range(self._hashTables)]
        
        #Loops through all games, for each game runs findHash and puts into specific bucket
        for i in range(numGames):
            game = self._dataSet[i]
            for t in range(self._hashTables):
                table = self._tables[t]
                hashKey = self.findHash(game, t)

                if hashKey not in table:
                    table[hashKey] = []
                
                table[hashKey].append(i)



    #Given a game vector and table index, determines and returns hash key
    def findHash(self, game: np.ndarray, tableIndex: int) -> tuple:

        #Ensures LSH is built
        if self.isBuilt() is False:
            raise RuntimeError("Error: Cannot hash game vector. Reason: LSH is not built")
        
        #Gives 2D array of all hyperplane vectors
        hyperplanes = self._hyperplanes[tableIndex]

        #Creates 1D array of dot product between all planes in the table and given game vector
        relativePos = hyperplanes.dot(game)

        #Creates hashKey tuple based on whether relativePos is >= 0 (above hyperplane) or < 0 (below hyperplane)
        hashKey = tuple(1 if p >= 0 else 0 for p in relativePos)
        return hashKey
    
    #Returns k nearest neighbors to provided game
    def findNeighbors(self, game: np.ndarray, k: int = 10) -> list[int]:

        #Ensures LSH is built
        if self.isBuilt() is False:
            raise RuntimeError("Error: Cannot hash game vector. Reason: LSH is not built")
        
        #Creates set to store potential neighbors to be compared later with cosine similarity 
        possibleNeighbors = set()

        #Loops through all tables for given game and adds the game's bucket to possibleNeighbors set
        for t in range(self._hashTables):
            table = self._tables[t]
            hashkey = self.findHash(game, t)
            bucket = table.get(hashkey, [])
            possibleNeighbors.update(bucket)
        
        if not possibleNeighbors:
            print("possibleNeighbors set is empty: Returning empty list")
            return []
        
        #Creates a python list from possibleNeighbors set then creates subvectors from thatlist
        pNList = list(possibleNeighbors)
        similarVectors = self._dataSet[pNList]

        #Cosine simularity by calculating dot product between each similar vector and the input game
        similars = similarVectors.dot(game)

        #Sorts similarity in decending order so highest similarity is index 0 then uses those indicies to fill neighbors list
        similarOrder = np.argsort(-similars)[0:k]
        neighbors = [pNList[v] for v in similarOrder]

        return neighbors

#Test/Debug area
if __name__ == "__main__":
    test = load_numpy_preprocessed_data()
    meta = load_metadata()
    norms = np.linalg.norm(test, axis=1)
    print("Min norm:", norms.min())
    print("Max norm:", norms.max())
    print("Index of max norm:", norms.argmax())

    testLSH = LSH()
    print(testLSH.isBuilt())

    start = time.perf_counter()
    testLSH.build(test)
    end = time.perf_counter()
    print(f"Time to build: {end - start} seconds")

    print(testLSH.isBuilt())

    
    start = time.perf_counter()
    print(testLSH.findNeighbors(test[100]))
    end = time.perf_counter()
    print(f"Time to find all neighbors: {end - start} seconds")