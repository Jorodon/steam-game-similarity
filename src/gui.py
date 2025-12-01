import time
import random
import pandas as pd
import streamlit as st
from guiHelpers import initRPForest, initLSH, initMetadata, indexFromName, showNeighbors, runQuery
from load_data import tuning_tree

def runGUI():
    st.title("Steam Game Similarity :material/joystick:")
    tab1, tab2 = st.tabs(["Similarity Search", "Performance History"])

    #Performance Trackers
    if "performanceHistory" not in st.session_state:
        st.session_state["performanceHistory"] = []

    if "buildTimes" not in st.session_state:
        st.session_state["buildTimes"] = {}

    metadata = initMetadata()
    with tab1:
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
            
            #Tracks querytime and method for random search
            st.session_state["performanceHistory"].append({"method": method, "queryTime": QueryTime})

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

            st.session_state["performanceHistory"]

            #Tracks querytime and method for normal search
            st.session_state["performanceHistory"].append({"method": method, "queryTime": QueryTime})

            #Shows QueryTime
            st.write(f"Took {QueryTime} seconds")
            #Shows neighbors to GUI
            showNeighbors(gameIndex, neighbors, metadata, method)

    with tab2:
        history = st.session_state["performanceHistory"]

        if not history:
            st.write("Run a search or random query to see timings.")

        else:
            #GRAPH SETUP & DISPLAY
            historyDF = pd.DataFrame(history)
            #Tracks query number by method so graph is comparative
            historyDF["queryNum"] = historyDF.groupby("method").cumcount() + 1

            st.subheader("Query times")
            chartDF = historyDF.pivot(index="queryNum", columns="method", values="queryTime")
            st.line_chart(chartDF)


        #Build Times Display
        st.subheader("Build times (cached)")
        buildTimes = st.session_state["buildTimes"]

        if not buildTimes:
            st.write("No models built yet.")

        else:
            for method, buildTime in buildTimes.items():
                st.write(f"{method}: {buildTime:.3f} seconds")

#To Do:
#- Stats


if __name__ == "__main__":
    runGUI()



