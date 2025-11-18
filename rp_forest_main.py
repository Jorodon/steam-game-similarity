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
    rp_tree = RPForest(initial_data, 50, 17, 15)
    rp_tree.createForest()

    #Tracks ending time of forest creation and prints result
    forest_create_end = time.time()
    time_passed = forest_create_end - forest_create_start
    print(f"Time to create forest is {time_passed}")

    # test_index = random.randint(0, 111452)
    # data_indices = rp_tree.traverseTree(test_index)
    # print(f"Test Index: {test_index}\nData Indices: {data_indices}")

if __name__ == "__main__":
    main()