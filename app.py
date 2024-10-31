import streamlit as st
import pandas as pd
import plotly.express as px
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import io
from PIL import Image

# Load the data
euro24_matches = sb.matches(season_id=282, competition_id=55)
euro24_matches['match'] = euro24_matches['competition_stage'] + ' : ' + euro24_matches['home_team'] + ' vs ' + euro24_matches['away_team']
unique_matches = euro24_matches['match'].unique().tolist()

# Streamlit UI for Match Selection
st.title("Euro 2024 Match Analysis")
match = st.selectbox("Select Match:", unique_matches)

# Filter shots based on selected match
if match:
    selected_match_id = euro24_matches[euro24_matches['match'] == match]['match_id'].values[0]
    df_shots = sb.events(match_id=selected_match_id)
    df_shots = df_shots[df_shots.type == 'Shot']

    
    # Dropdown for shot selection
    shot_id = st.selectbox("Select Shot ID:", df_shots['id'].unique())
    
    # Plot pitch with shot information
    if shot_id:
        selected_shot1 = df_shots[df_shots.id == shot_id].iloc[0].reset_index(drop=True)
        selected_shot = df_shots[df_shots.id == shot_id].iloc[0].reset_index(drop=True)


        data = selected_shot.at[0, 'shot_freeze_frame']
    
    # Check if data is a list, otherwise skip the iteration
        if isinstance(data, list):
        # Convert to DataFrame
                df = pd.DataFrame([{
                    'location_x': item['location'][0],
                    'location_y': item['location'][1],
                    'player_name': item['player']['name'],
                    'teammate': item['teammate']
                        } for item in data])

        
        selected_shot=pd.concat([selected_shot] * df.shape[0], ignore_index=True)

        
        # Create pitch plot
        pitch = Pitch(pitch_type='statsbomb', pitch_color='black', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 6))
        ax.set_xlim(75, 130)

        # Plot shot details
        x, y = selected_shot1['location']
        end_x, end_y = selected_shot1['shot_end_location'][:2]
        plt.plot((x, end_x), (y, end_y), color="yellow", linestyle='--')
        plt.scatter(x, y, color='yellow', marker='o')
        for i in range(len(selected_shot)):
                    # Location markers based on teammate status
            if df_each_shoot.iloc[i]['teammate']:
                plt.scatter(selected_shot.iloc[i]['location_x'], df_each_shoot.iloc[i]['location_y'], color='green')
            else:
                plt.scatter(df_each_shoot.iloc[i]['location_x'], df_each_shoot.iloc[i]['location_y'], color='red')
    
    # Add dummy points for legend only
        plt.scatter([], [], color='yellow', marker='o', label='Shooter')
        plt.scatter([], [], color='green', marker='o', label='Attackers')
        plt.scatter([], [], color='red', marker='o', label='Difenders')






        
        # Convert plot to image for Streamlit display
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        image = Image.open(buf)
        st.image(image, caption="Shot Visualization", use_column_width=True)
        
        # Display shot details in a table format
        st.write(f"**Shot Time:** {selected_shot['timestamp']}")
        st.write(f"**Team:** {selected_shot['team']}")
        st.write(f"**Player:** {selected_shot['player']}")
        st.write(f"**Shot Outcome:** {selected_shot['shot_outcome']}")
        st.write(f"**Expected Goals (xG):** {selected_shot['shot_statsbomb_xg']}")
