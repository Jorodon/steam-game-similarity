import time
import random
import streamlit as st
from guiHelpers import initRPForest, initLSH, initMetadata, indexFromName, showNeighbors

def main():
    st.title("Steam Game Similarity :material/joystick:")

    metadata = initMetadata()
    LSH = initLSH()
    #RPForest = initRPForest()
    LSHQueryTime = 0.00

    #Method dropdown
    available_methods = ["LSH", "RP Forest", "Brute"]
    method = st.selectbox("Method", available_methods)

    #Game searchbox
    game_name = st.text_input("Game name")

    #Amount of similar games slider
    k = st.slider("Number of similar games", 5, 30, 10)


    #BUTTONS
    left, middle, right = st.columns(3)
    #Search button that checks for game index using helper function
    if left.button("Search", width="stretch", icon=":material/search:") and game_name:   
        gameIndex = indexFromName(game_name, metadata)
        if gameIndex is None:
            st.error(f"Error: Game '{game_name}' not found!")
            return
        
        #LSH Method
        if method == "LSH":
            start = time.perf_counter()
            neighbors = LSH.findNeighborsFromIndex(gameIndex, k)
            end = time.perf_counter()
            LSHQueryTime = round(end - start, 5)
        
    #Shows neighbors to GUI
    st.subheader(f"Took {LSHQueryTime} seconds")
    showNeighbors(gameIndex, neighbors, metadata)

    #Random button that uses random game
    random = middle.button("Random", width="stretch", icon=":material/shuffle:")
    #Reset button
    reset = right.button("Reset", type="primary", width="stretch", icon=":material/replay:")


    

#To Do:
#- Dropdown for RP Forest, LSH, or both
#- Random game name or search
#- Stats


if __name__ == "__main__":
    main()



