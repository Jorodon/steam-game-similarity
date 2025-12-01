import load_data
import time
from rp_forest import RPForest
from lsh import LSH
from load_data import tuning_tree
import streamlit as st

@st.cache_resource
def initRPForest():
    start = time.perf_counter()

    #RPForest load and setup
    forestData = load_data.load_preprocessed_data()
    rpForest = RPForest(forestData, 15, 14, 50)
    rpForest.createForest(useMP=False)

    end = time.perf_counter()

    buildTime = end - start
    return rpForest, buildTime

@st.cache_resource
def initLSH():
    start = time.perf_counter()

    #LSH load and setup
    lshData = load_data.load_numpy_preprocessed_data()
    lshModel = LSH(10, 16)
    lshModel.build(lshData)
    
    end = time.perf_counter()

    buildTime = end - start
    return lshModel, buildTime

@st.cache_resource
def initMetadata():
    #metadata load
    metadata = load_data.load_metadata()

    return metadata


def indexFromName(name: str, metadata: dict):
    #strips whitespace and all lowercase for consistent searches
    name = name.strip().lower()
    
    #Loops through each item in metadata and returns index if the name matches
    for i in metadata.items():
        gameIndex = i[0]
        gameValues = i[1]
        if gameValues.get("Name").lower() == name:
            return int(gameIndex)
    
    return None


def showNeighbors(gameIndex: int, neighbors: list[int], metadata: dict):
    #Metadata for main game
    mainMeta = metadata.get(str(gameIndex))
    mainName = mainMeta.get("Name")

    #Gui printout
    st.subheader(f"Results for {mainName}: ")

    #Grabs index and uses enumerate to display rank
    for rank, index in enumerate(neighbors, start=1):
        meta = metadata.get(str(index))
        name = meta.get("Name")
        st.write(f"{rank}: {name}")

def runQuery(method: str, index: int, k: int):
    #LSH Method
    if method == "LSH":
        #Builds LSH and returns LSH & time to build
        LSH, buildTime = initLSH()
        
        #Times Query
        start = time.perf_counter()
        neighbors = LSH.findNeighborsFromIndex(index, k)
        end = time.perf_counter()
        
        QueryTime = round(end - start, 5)
    
    #RP Forest Method
    elif method == "RP Forest":
        RPForest, buildTime = initRPForest()

        #Times Query
        start = time.perf_counter()
        neighbors = RPForest.traverseForest(index, k)
        end = time.perf_counter()

        QueryTime = round(end - start, 5)
    
    #Brute Method
    elif method == "Brute":
        #Times Query
        start = time.perf_counter()
        neighbors = tuning_tree(index, k)
        end = time.perf_counter()

        QueryTime = round(end - start, 5)
    
    
    else:
        neighbors = None
        QueryTime = None
        st.error("Error: Method not found!", icon="🚨")
    
    return neighbors, QueryTime