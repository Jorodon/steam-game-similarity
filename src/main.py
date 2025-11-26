import random
import time
import load_data_test
from rp_tree import RPTree
from rp_forest import RPForest


#Full main method for random projection forest
def main():
    #Tracks time to create a forest
    forest_create_start = time.time()

    #Loads preprocessed data and creates a RPForest using it
    initial_data = load_data_test.load_preprocessed_data()
    rp_forest = RPForest(initial_data, 50, 17, 15)
    rp_forest.createForest()

    #Tracks ending time of forest creation and prints result
    forest_create_end = time.time()
    time_passed = forest_create_end - forest_create_start
    print(f"Time to create forest is {time_passed}")

    '''REMOVE/REPLACE count/while loop'''
    count = 0
    while count < 10:
        '''REMOVE/REPLACE WITH ACTUAL INPUT'''
        test_index = random.randint(0, 111452)

        #Tracks time to query the forest
        forest_traverse_start = time.time()

        #Finds k nearest neighbors in forest
        data_indices = rp_forest.traverseForest(test_index, 10)

        #Tracks ending time of query and prints results
        forest_traverse_end = time.time()
        time_passed = forest_traverse_end - forest_traverse_start
        #print(f"Test Index: {test_index}\nData Count: {len(data_indices)}\nData Indices: {data_indices}")

        '''REMOVE GAME/BRUTE FORCE PRINT OUTPUTS - REPLACE WITH GUI'''
        #Loading the metadata to display the game names
        metadata_dict = load_data_test.load_metadata()
        search_name = metadata_dict.get(str(test_index)).get("Name")
        game_names = [metadata_dict.get(str(key)).get("Name") for key in data_indices]
        print(f"Data Count: {len(data_indices)}\nGame Searched: {search_name}\n\nTime to query forest is {time_passed}\nGames: {game_names}")

        #Uses brute force method to find the k-most-similar games
        nearest_neighbors = load_data_test.tuning_tree(test_index, 10)
        
        #Outputs brute force results
        game_names_brute = [metadata_dict.get(str(key)).get("Name") for key in nearest_neighbors]
        print(f"Brute Force Games: {game_names_brute}\n\n")

        count += 1

    

if __name__ == "__main__":
    main()