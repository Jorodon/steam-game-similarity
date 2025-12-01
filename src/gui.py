import time
import random
import streamlit as st
from guiHelpers import initRPForest, initLSH, initMetadata, indexFromName, showNeighbors, runQuery
from load_data import tuning_tree

def runGUI():
    st.title("Steam Game Similarity :material/joystick:")

    #Performance Trackers
    if "performanceHistory" not in st.session_state:
        st.session_state["perfHistory"] = []

    if "buildTimes" not in st.session_state:
        st.session_state["buildTimes"] = {}
    
    metadata = initMetadata()

    #Method dropdown
    available_methods = ["LSH", "RP Forest", "Brute"]
    method = st.selectbox("Method", available_methods)

    #Game searchbox
    game_name = st.text_input("Game name")

    #Amount of similar games slider
    k = st.slider("Number of similar games", 5, 30, 10)


    #BUTTONS
    left, middle, right = st.columns(3)

    #Random button that uses random game
    if middle.button("Random", width="stretch", icon=":material/shuffle:"):
        #Gets a random key from metadata and converts to int
        randomIndex = int(random.choice(list(metadata.keys())))
        neighbors = None

        #Gets metadata/name from randomIndex
        gameMetadata = metadata.get(str(randomIndex))
        randomName = gameMetadata.get('Name')

        #shows random game picked on GUI
        st.info(f"Random game picked: {randomName}")

        neighbors, QueryTime = runQuery(method, randomIndex, k)

        #Shows QueryTime
        st.write(f"Took {QueryTime} seconds")
        #Shows neighbors to GUI
        showNeighbors(randomIndex, neighbors, metadata, method)

    #Clear button
    if right.button("Clear", type="primary", width="stretch", icon=":material/replay:"):
        st.session_state.clear()
        st.info("Cleared Interface")
        
    #Search button that checks for game index using helper function
    if left.button("Search", width="stretch", icon=":material/search:") and game_name:   
        gameIndex = indexFromName(game_name, metadata)
        if gameIndex is None:
            st.error(f"Error: Game '{game_name}' not found!", icon="🚨")
            return
        
        #shows game picked on GUI
        st.info(f"Game picked: {game_name}")

        neighbors, QueryTime = runQuery(method, gameIndex, k)

        #Shows QueryTime
        st.write(f"Took {QueryTime} seconds")
        #Shows neighbors to GUI
        showNeighbors(gameIndex, neighbors, metadata, method)


    

#To Do:
#- Stats


if __name__ == "__main__":
    runGUI()



