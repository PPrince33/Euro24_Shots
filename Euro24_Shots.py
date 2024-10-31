import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsbombpy import sb
from mplsoccer import Pitch
import streamlit as st

# Load data
euro24 = list(sb.matches(season_id=282, competition_id=55)['match_id'])
euro24_matches = sb.matches(season_id=282, competition_id=55)
euro24_matches = euro24_matches[['match_id', 'home_team', 'home_score', 'away_team', 'away_score', 'competition_stage']]

df_main = pd.DataFrame()
for i in euro24:
    data = sb.events(match_id=i)
    df_main = pd.concat([data, df_main], ignore_index=True)

df_shots = df_main[df_main.type == 'Shot']
df_shots = df_shots[['id', 'timestamp', 'match_id', 'player', 'team', 'shot_freeze_frame', 'shot_type', 'shot_outcome', 'shot_statsbomb_xg', 'location', 'shot_end_location']]

euro24_matches['match'] = euro24_matches['competition_stage'] + ' : ' + euro24_matches['home_team'] + ' vs ' + euro24_matches['away_team']

df_shots = pd.merge(df_shots, euro24_matches[['match_id', 'match']], on='match_id', how='left')

# Streamlit app layout
st.title("Euro 2024 Shot Analysis")

# Match selection dropdown
unique_matches = euro24_matches['match'].unique().tolist()
selected_match = st.selectbox("Select Match:", unique_matches)

# Get events for the selected match
selected_match_events = df_shots[df_shots.match == selected_match].reset_index(drop=True)

# Shot selection dropdown
if not selected_match_events.empty:
    unique_shots = selected_match_events['id'].unique().tolist()
    selected_shot = st.selectbox("Select Shot ID:", unique_shots)
    
    all_shots = pd.DataFrame()
    
    for i in selected_match_events.index:
        data = selected_match_events.at[i, 'shot_freeze_frame']
        
        if isinstance(data, list):
            df = pd.DataFrame([{
                'location_x': item['location'][0],
                'location_y': item['location'][1],
                'player_name': item['player']['name'],
                'teammate': item['teammate']
            } for item in data])
            
            event_info_df = pd.DataFrame([selected_match_events.iloc[i]])
            event_info_df = pd.concat([event_info_df] * df.shape[0], ignore_index=True)
            df = pd.concat([event_info_df, df], axis=1)
            all_shots = pd.concat([all_shots, df], axis=0, ignore_index=True)

    all_shots['shot_end_location'] = all_shots['shot_end_location'].apply(lambda x: tuple(x) if isinstance(x, list) else x)
    all_shots['location'] = all_shots['location'].apply(lambda x: tuple(x) if isinstance(x, list) else x)

    # Extract coordinates
    all_shots['X'] = all_shots['location'].apply(lambda loc: loc[0])
    all_shots['Y'] = all_shots['location'].apply(lambda loc: loc[1])
    all_shots['endX'] = all_shots['shot_end_location'].apply(lambda loc: loc[0])
    all_shots['endY'] = all_shots['shot_end_location'].apply(lambda loc: loc[1])
    all_shots['endZ'] = all_shots['shot_end_location'].apply(lambda loc: loc[2] if len(loc) > 2 else None)
    all_shots.drop(columns={'shot_freeze_frame', 'location', 'shot_end_location'}, inplace=True)

    # Function to plot shots
    def plot_shots(shot_id):
        df_each_shoot = all_shots[all_shots.id == shot_id].reset_index(drop=True)
        if df_each_shoot.empty:
            st.write("No data available for the selected shot.")
            return
        
        df_each_shoot_time = df_each_shoot.timestamp.unique()[0]
        df_each_shoot_shooter = df_each_shoot.player.unique()[0]
        df_each_shoot_shot_outcome = df_each_shoot.shot_outcome.unique()[0]
        df_each_shoot_team = df_each_shoot.team.unique()[0]

        # Create the pitch
        pitch = Pitch(pitch_type='statsbomb', pitch_color='black', line_color='white')
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor("black")
        ax.set_xlim(75, 130)

        for i in range(len(df_each_shoot)):
            plt.plot((df_each_shoot.iloc[i]['X'], df_each_shoot.iloc[i]['endX']),
                     (df_each_shoot.iloc[i]['Y'], df_each_shoot.iloc[i]['endY']),
                     color="yellow", ls='--')
            
            plt.scatter(df_each_shoot.iloc[i]['X'], df_each_shoot.iloc[i]['Y'], color='yellow', marker='o')
            
            if df_each_shoot.iloc[i]['teammate']:
                plt.scatter(df_each_shoot.iloc[i]['location_x'], df_each_shoot.iloc[i]['location_y'], color='green')
            else:
                plt.scatter(df_each_shoot.iloc[i]['location_x'], df_each_shoot.iloc[i]['location_y'], color='red')

        # Add dummy points for legend only
        plt.scatter([], [], color='yellow', marker='o', label='Shooter')
        plt.scatter([], [], color='green', marker='o', label='Attacking')
        plt.scatter([], [], color='red', marker='o', label='Defending')

        plt.title(f"{selected_match_events['match'].iloc[0]}\n{df_each_shoot_team} - {df_each_shoot_shooter} (Outcome: {df_each_shoot_shot_outcome})", color='white')
        st.pyplot(fig)

    plot_shots(selected_shot)
else:
    st.write("No shots available for the selected match.")
