
# Steam Game Similarity Search

Find your next favorite Steam game by example — type a title for a game you like, and this app finds similar titles using one of three different nearest-neighbor search methods (brute force nearest neighbor and custom implemented RP Forest and LSH). Performance metrics allow you to track time to query across all three methods and see build times for LSH and RP Forest.


## Table Of Contents

1. Getting Started [Link text](#getting-started)
    - 1.1 Webapp [Link text](#use-webapp)
    - 1.2 Host Locally [Link text](#host-locally)
2. Usage/Examples [Link text](#usage/examples)
    - 2.1 Similarity Search Tab [Link text](#similarity-search-tab)
    - 2.2 Performance History Tab [Link text](#performance-history-tab)
    - 2.3 Developer Info Tab [Link text](#developer-info-tab)
3. Documentation [Link text](#documentation)
4. Authors [Link text](#authors)
## Getting Started
---

Getting started is super easy! Either visit our webapp hosted via streamlit or host the app locally. Hosting the app locally will have more consistent query times and have approximately 50% faster build times and queries.

### 1. Use Webapp:

Visit the webapp at https://steamgame.streamlit.app/

### 2. Host Locally:

**Step 1:**

Clone the repository locally
 ```bash
   git clone https://github.com/<your-username>/steam-game-similarity.git
   cd steam-game-similarity
```
After cloning, it is recommended to use a virtual environment. (Ensure you run these lines from the local repository folder)
- Windows
```bash
py -m venv .venv
.venv\Scripts\activate
```
- macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**Step 2:**

Install dependencies
- Windows
```bash
pip install -r requirements.txt
```
- macOS / Linux
```bash
pip3 install -r requirements.txt
```

**Step 3:**

Start the app locally
```bash
streamlit run src/gui.py
```

This will open a locally hosted version of the app in your default browser.


## Usage/Examples
---


Once you've got the app running either locally or via the webapp, you'll be met with three tabs.

### 1. Similarity Search Tab
    This tab has most of the main app functionality

    + **Pick a method from the dropdown**
        - "LSH" -> Locality-sensitive hashing (Fast, approximate search)
        - "RP Forest" -> Random Projection Forest (Fast, approximate search)
            > This will take a couple of minutes to build, but gets stored in the cache
        - "Brute" - Brute Force (Exact baseline) 
    + **Set how many results you want**
        - Choose how many similar games to show with the *Number of similar games* slider
    + **Choose a game**
        - Type a game title into the *Game name* box
        - Or hit *Random* to let the app pick a random game from the dataset
    + **Click Search**
        - The app will show the amount of similar games below
    
![Search demo](assets/search-demo.gif)
---
### 2. Performance History Tab
    
    This tab tracks query times and build times for comparisons

    + Every search and random query will log:
        - Which **method** was used
        - The **query time**
        - The **game index**
        - The **game name** (Manual search only)
    
    + These results are displayed on a graph
        - Top right of the graph has a table/graph toggle
    + Reset button will clear the query time cache
        - Warning prompt will ask if you are sure you want to clear that cache
    + Run Random button will run a random search for all three methods
        - Clicking will display a slider asking how many random queries to run
        - After selecting the amount, hit the *Run Test* button
    
    + The bottom of the screen will display the build times for the cached LSH and RP Forest structures

![Graph demo](assets/search-demo.gif)
---
### 3. Developer Info Tab 
    This tab will display the session_state cache. Mainly used for debugging/testing

    + **Index to Game Name Search**
        - This allows a game index input that returns the game title from the metadata
    + **Display area for the session_state cache**
        - Allows for easy access to all data in session_state (Often used with *Index to Game Name Search*)

![Dev demo](assets/developer-demo.gif)
## Documentation
---

[Documentation](https://linktodocumentation)


## Authors

- [@Jorodon](https://github.com/Jorodon)
- [@Colbygrimmscott](https://github.com/Colbygrimmscott)

