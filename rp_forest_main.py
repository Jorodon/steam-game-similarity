import random
import load_data_test
from rp_tree import RPTree
from rp_forest import RPForest


#Test main method
def main():
    #Loads preprocessed data and creates an RPTree using it
    initial_data = load_data_test.load_preprocessed_data()
    rp_tree = RPTree(initial_data, 17, 15)
    rp_tree.createTree()

    #Tests if tree creation works properly
    rp_tree.outputDictDebug()

    test_index = random.randint(0, 111452)
    data_indices = rp_tree.traverseTree(test_index)
    print(f"Test Index: {test_index}\nData Indices: {data_indices}")

if __name__ == "__main__":
    main()