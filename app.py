import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np

st.title('NBA Stats Player Explorer')

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2025))))

@st.cache_data
def load_data(year): 
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_game.html'
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats

player_stats = load_data(selected_year)

sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)


unique_pos = ['PG', 'SG', 'SF', 'PF', 'C']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team = player_stats[(player_stats.Tm.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Teams')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team)

# downloading csv file
def filedownload(df): 
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv"> Download CSV File</a>'
    return href
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

if st.button('Intercorrelation Heatmap'): 
    st.header('Intercorrelation Matrix Heatmap')
    # df_selected_team.to_csv('output.csv', index=False)
    # df = pd.read_csv('output.csv')
    
    corr = df_selected_team.corr()

    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style("white"): 
        f, ax = plt.subplots(figsize = (7,5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f) 