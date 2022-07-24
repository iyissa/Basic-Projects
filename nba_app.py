import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.static import players 
from nba_api.stats.endpoints import commonplayerinfo
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.set_option('deprecation.showPyplotGlobalUse', False)

st.write("""
Hello """)

def get_player_data(id):
    player_id = commonplayerinfo.CommonPlayerInfo(id)
    player_id_df = player_id.player_headline_stats.get_data_frame()
    res = pd.DataFrame(player_id_df)
    return res

def find_player_id(name):
    """
    A function to go in and return the id of a given player
    """
    player_name = players.find_players_by_full_name(name)
    return player_name[0]['id']
    

def edit_multiple_player_id(player_list):
    """
    A function to get the player id of a list of players from the NBA_API
    """
    mood = []
    for i in player_list:
        oid = find_player_id(i)
        mood.append(oid)
    return mood

def edit_make_dataset(player_dataset):
    result = pd.DataFrame()
    for i in player_dataset:
        each_player = get_player_data(i)
        result = pd.concat([result, each_player])
    return result

def plot_viz(viz_dataset):
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 6))

    # Points per Game
    sns.set_color_codes("pastel")
    sns.barplot(x="PTS", y="PLAYER_NAME", data=viz_dataset, label="PPG", color="b")

    # Assist per game
    sns.set_color_codes("muted")
    sns.barplot(x="AST", y="PLAYER_NAME", data=viz_dataset, label="APG", color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 30), ylabel="Players", xlabel="Per Game Stats")
    sns.despine(left=True, bottom=True)

def everything(data):
    final_player_id = edit_multiple_player_id(player_list=data)
    print("Gotten Player ID")

    print("Creating Dataset ... ")
    final_player_dataset = edit_make_dataset(player_dataset=final_player_id)
    print("Created Dataset")

    print("Plotting Visualization ...")

    plot_viz(viz_dataset=final_player_dataset)
    print("My work here is done chief")

def convert(names):
    name_list = [name.strip() for name in names.split(",")]
    return name_list

soft = st.text_input(" ")

very_soft = str(soft)

yo = convert(very_soft)
print(yo)

#print(edit_make_dataset(yo))
everything(yo)
st.pyplot()
