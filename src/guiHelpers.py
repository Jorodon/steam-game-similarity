import load_data
from rp_forest import RPForest
from lsh import LSH
import streamlit as st

@st.cache_resource
def initRPForest():
    #RPForest load and setup
    forestData = load_data.load_preprocessed_data()
    rpForest = RPForest(forestData, 50, 17, 15)
    rpForest.createForest()

    return rpForest

@st.cache_resource
def initLSH():
    #LSH load and setup
    lshData = load_data.load_numpy_preprocessed_data()
    lshModel = LSH(10, 16)
    lshModel.build(lshData)

    return lshModel

@st.cache_resource
def initMetadata():
    #metadata load
    metadata = load_data.load_metadata()

    return metadata