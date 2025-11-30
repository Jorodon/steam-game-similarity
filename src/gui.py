import time
import streamlit as st
from guiHelpers import initRPForest, initLSH, initMetadata, indexFromName

RPForest = initRPForest()
LSH = initLSH()
metadata = initMetadata()

#To Do:
'''
- Dropdown for RP Forest, LSH, or both
- Random game name or search
- Stats
'''

if __name__ == "__main__":
    print(indexFromName("BrainTeaser", metadata))



