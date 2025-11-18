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
    rp_forest = RPForest(initial_data, 5, 17, 15)
    rp_forest.createForest()

    #Tracks ending time of forest creation and prints result
    forest_create_end = time.time()
    time_passed = forest_create_end - forest_create_start
    print(f"Time to create forest is {time_passed}")

    test_index = random.randint(0, 111452)
    test_index = 31341
    data_indices = rp_forest.traverseForest(test_index, 10)
    #print(f"Test Index: {test_index}\nData Count: {len(data_indices)}\nData Indices: {data_indices}")

    #Loading the metadata to display the game names
    metadata_dict = load_data_test.load_metadata()
    search_name = metadata_dict.get(str(test_index)).get("Name")
    game_names = [metadata_dict.get(str(key)).get("Name") for key in data_indices]
    print(f"Data Count: {len(data_indices)}\nGame Searched: {search_name}\nGames: {game_names}")


if __name__ == "__main__":
    main()