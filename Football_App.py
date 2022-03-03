import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64

st.title( " Composite Big 5 Leagues ")

st.markdown ( """
This web-app's function is to show the complete league table of the top 5 European leagues arranged by order of points per match 

Leagues available are England, Spain, Germany, France, Italy
(League data available from 1990-Present)

""")

st.sidebar.header("What is it you desire?")
unique_pos = st.sidebar.selectbox('League Rank', list(reversed(range(1,21))))

st.write(' ### Kindly Input The Season You Would Like to Check ' )
st.write(' The format should be of the form 2018-2019')
st.write(' The default year on load up of page is 2021-2022 season')

st.header("Input text below")
selected_year = st.text_input(" ")

# Web Scraping
@st.cache
def load_data(selected_year):
    url = "https://fbref.com/en/comps/Big5/" + str(selected_year) + "/" + str(selected_year) + "-Big-5-European-Leagues-Stats"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df
playerstats = load_data(selected_year)

# Sidebar - Country selection
sorted_unique_team = sorted(playerstats.Country.unique())
selected_team = st.sidebar.multiselect('Country', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = sorted(playerstats.LgRk.unique())

selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data

df_selected_team = playerstats[(playerstats.Country.isin(selected_team)) & (playerstats.LgRk.isin(selected_pos))] #& (playest.header('Display Player Stats of Selected Team(s)')
st.header("Big 5 Leagues Data")
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
test=df_selected_team.astype(str)
st.dataframe(test)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)


if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    st.set_option('deprecation.showPyplotGlobalUse', False)
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
    



st.markdown("""
* **Python-libraries used:** pandas, streamlit, base64
* **Data Source:** [Fbref.com](https://fbref.com/en/)
"""
)