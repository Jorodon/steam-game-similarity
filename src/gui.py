import time
import streamlit as st
from guiHelpers import initRPForest, initLSH, initMetadata, indexFromName

def main():
    st.title("Steam Game Similarity")

    metadata = initMetadata()
    LSH = initLSH()
    #RPForest = initRPForest()

    #Method dropdown
    available_methods = ["LSH"]
    method = st.selectbox("Method", available_methods)

    #Game searchbox
    game_name = st.text_input("Game name")

    #Amount of similar games slider
    k = st.slider("Number of similar games", 5, 30, 10)

    

#To Do:
#- Dropdown for RP Forest, LSH, or both
#- Random game name or search
#- Stats


if __name__ == "__main__":
    main()



