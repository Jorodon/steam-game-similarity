import time
import random
import pandas as pd
import streamlit as st
from guiHelpers import initRPForest, initLSH, initMetadata, indexFromName, showNeighbors, runQuery
from load_data import tuning_tree

#GLOBALS
RPForestWarning = True

#Warning for resetting graph
@st.dialog("Reset Warning ⚠️")
def resetGraph():
    st.write("This will delete all previous preformance cache.\n\nAre you sure you want to clear it?")
    left2, right2 = st.columns(2)
    #Cancel button
    if right2.button("Cancel", type="primary", width="stretch"):
        st.rerun()
    
    #Proceed button (resets performanceHistory in session state)
    if left2.button("Proceed", width="stretch"):
        with st.spinner("Resetting graph...", show_time=True):
            st.session_state["performanceHistory"] = []
        st.success("Reset successfully!")
        st.rerun()

def runGUI():
    st.title("Steam Game Similarity :material/joystick:")
    tab1, tab2, tab3 = st.tabs(["Similarity Search", "Performance History", "Developer Info"])

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
            with st.spinner("Running Query... Please wait! This may take a while if building for the first time.", show_time=True):
                neighbors, QueryTime = runQuery(method, randomIndex, k)
            st.success("Done!")
            
            #Tracks querytime and method for random search
            st.session_state["performanceHistory"].append({"method": method, "queryTime": QueryTime, "gameIndex": randomIndex, "gameName": randomName})

            #Shows QueryTime
            st.write(f"Took {QueryTime} seconds")
            #Shows neighbors to GUI
            showNeighbors(randomIndex, neighbors, metadata, method)

        #Clear button
        if right.button("Clear", type="primary", width="stretch", icon=":material/replay:"):
            st.rerun()
            
        #Search button that checks for game index using helper function
        if left.button("Search", width="stretch", icon=":material/search:") and game_name:   
            gameIndex = indexFromName(game_name, metadata)
            neighbors = None

            if gameIndex is None:
                st.error(f"Error: Game '{game_name}' not found!", icon="🚨")
                return
            
            #shows game picked on GUI
            st.info(f"Game picked: {game_name}")

            with st.spinner("Running Query... Please wait! This may take a while if building for the first time.", show_time=True):
                neighbors, QueryTime = runQuery(method, gameIndex, k)
            st.success("Done!")

            #Tracks querytime and method for normal search
            st.session_state["performanceHistory"].append({"method": method, "queryTime": QueryTime, "gameIndex": gameIndex, "gameName": game_name})

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

            if st.button("Reset Graph", type="primary", icon=":material/replay:"):
                resetGraph()
                
        with st.popover("Run Random", icon=":material/shuffle:"):
            randomRuns = st.slider("Choose amount of queries to run:", 5, 100, 10)
            if st.button("Run Test", icon=":material/timer_play:"):
                #Loading text
                with st.spinner("Running test...", show_time=True):
                    #Runs each algorithm for k times
                    for i in range (randomRuns):
                        randomIndex = int(random.choice(list(metadata.keys())))
                        neighbors = None

                        #LSH
                        neighbors, QueryTime = runQuery("LSH", randomIndex, k)
                        st.session_state["performanceHistory"].append({"method": "LSH", "queryTime": QueryTime, "gameIndex": randomIndex})

                        #RP Forest
                        neighbors, QueryTime = runQuery("RP Forest", randomIndex, k)
                        st.session_state["performanceHistory"].append({"method": "RP Forest", "queryTime": QueryTime, "gameIndex": randomIndex})

                        #Brute
                        neighbors, QueryTime = runQuery("Brute", randomIndex, k)
                        st.session_state["performanceHistory"].append({"method": "Brute", "queryTime": QueryTime, "gameIndex": randomIndex})
                
                #Shows done and refreshes
                st.success("Done!")
                time.sleep(0.5)
                st.rerun()
    
        #Build Times Display
        st.subheader("Build times (cached)")
        buildTimes = st.session_state["buildTimes"]

        if not buildTimes:
            st.write("No models built yet.")

        else:
            for method, buildTime in buildTimes.items():
                st.write(f"{method}: {buildTime:.3f} seconds")

    with tab3:
        st.header("Developer Tools")
        
        #Index to Game Name Deve Tool
        st.write("Index to Game Name Search")
        gameIndexDev = st.text_input("Input Index:")
        gameNameDev = None
        if st.button("Search Index", width="stretch", icon=":material/search:") and gameIndexDev:
            with st.spinner("Running test...", show_time=True):   
                gameMetadataDev = metadata.get(str(gameIndexDev))
                if gameMetadataDev == None:
                    st.error(f"Error: Game at index '{gameIndexDev}' not found!", icon="🚨")
                    return
                gameNameDev = gameMetadataDev.get('Name')
            st.success("Complete!")
        if gameNameDev:
            st.write(f'Game with index {gameIndexDev} is "{gameNameDev}"!')

        #Cache List
        st.write("Session state cache:")
        st.write(st.session_state)

if __name__ == "__main__":
    runGUI()



