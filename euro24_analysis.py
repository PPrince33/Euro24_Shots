{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "587a8a4f-9090-4824-ae14-e3fae0ec22f2",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from statsbombpy import sb\n",
    "from mplsoccer import Pitch\n",
    "import streamlit as st\n",
    "\n",
    "# Load data\n",
    "euro24 = list(sb.matches(season_id=282, competition_id=55)['match_id'])\n",
    "euro24_matches = sb.matches(season_id=282, competition_id=55)\n",
    "euro24_matches = euro24_matches[['match_id', 'home_team', 'home_score', 'away_team', 'away_score', 'competition_stage']]\n",
    "\n",
    "df_main = pd.DataFrame()\n",
    "for i in euro24:\n",
    "    data = sb.events(match_id=i)\n",
    "    df_main = pd.concat([data, df_main], ignore_index=True)\n",
    "\n",
    "df_shots = df_main[df_main.type == 'Shot']\n",
    "df_shots = df_shots[['id', 'timestamp', 'match_id', 'player', 'team', 'shot_freeze_frame', 'shot_type', 'shot_outcome', 'shot_statsbomb_xg', 'location', 'shot_end_location']]\n",
    "\n",
    "euro24_matches['match'] = euro24_matches['competition_stage'] + ' : ' + euro24_matches['home_team'] + ' vs ' + euro24_matches['away_team']\n",
    "\n",
    "df_shots = pd.merge(df_shots, euro24_matches[['match_id', 'match']], on='match_id', how='left')\n",
    "\n",
    "# Streamlit app layout\n",
    "st.title(\"Euro 2024 Shot Analysis\")\n",
    "\n",
    "# Match selection dropdown\n",
    "unique_matches = euro24_matches['match'].unique().tolist()\n",
    "selected_match = st.selectbox(\"Select Match:\", unique_matches)\n",
    "\n",
    "# Get events for the selected match\n",
    "selected_match_events = df_shots[df_shots.match == selected_match].reset_index(drop=True)\n",
    "\n",
    "# Shot selection dropdown\n",
    "if not selected_match_events.empty:\n",
    "    unique_shots = selected_match_events['id'].unique().tolist()\n",
    "    selected_shot = st.selectbox(\"Select Shot ID:\", unique_shots)\n",
    "    \n",
    "    all_shots = pd.DataFrame()\n",
    "    \n",
    "    for i in selected_match_events.index:\n",
    "        data = selected_match_events.at[i, 'shot_freeze_frame']\n",
    "        \n",
    "        if isinstance(data, list):\n",
    "            df = pd.DataFrame([{\n",
    "                'location_x': item['location'][0],\n",
    "                'location_y': item['location'][1],\n",
    "                'player_name': item['player']['name'],\n",
    "                'teammate': item['teammate']\n",
    "            } for item in data])\n",
    "            \n",
    "            event_info_df = pd.DataFrame([selected_match_events.iloc[i]])\n",
    "            event_info_df = pd.concat([event_info_df] * df.shape[0], ignore_index=True)\n",
    "            df = pd.concat([event_info_df, df], axis=1)\n",
    "            all_shots = pd.concat([all_shots, df], axis=0, ignore_index=True)\n",
    "\n",
    "    all_shots['shot_end_location'] = all_shots['shot_end_location'].apply(lambda x: tuple(x) if isinstance(x, list) else x)\n",
    "    all_shots['location'] = all_shots['location'].apply(lambda x: tuple(x) if isinstance(x, list) else x)\n",
    "\n",
    "    # Extract coordinates\n",
    "    all_shots['X'] = all_shots['location'].apply(lambda loc: loc[0])\n",
    "    all_shots['Y'] = all_shots['location'].apply(lambda loc: loc[1])\n",
    "    all_shots['endX'] = all_shots['shot_end_location'].apply(lambda loc: loc[0])\n",
    "    all_shots['endY'] = all_shots['shot_end_location'].apply(lambda loc: loc[1])\n",
    "    all_shots['endZ'] = all_shots['shot_end_location'].apply(lambda loc: loc[2] if len(loc) > 2 else None)\n",
    "    all_shots.drop(columns={'shot_freeze_frame', 'location', 'shot_end_location'}, inplace=True)\n",
    "\n",
    "    # Function to plot shots\n",
    "    def plot_shots(shot_id):\n",
    "        df_each_shoot = all_shots[all_shots.id == shot_id].reset_index(drop=True)\n",
    "        if df_each_shoot.empty:\n",
    "            st.write(\"No data available for the selected shot.\")\n",
    "            return\n",
    "        \n",
    "        df_each_shoot_time = df_each_shoot.timestamp.unique()[0]\n",
    "        df_each_shoot_shooter = df_each_shoot.player.unique()[0]\n",
    "        df_each_shoot_shot_outcome = df_each_shoot.shot_outcome.unique()[0]\n",
    "        df_each_shoot_team = df_each_shoot.team.unique()[0]\n",
    "\n",
    "        # Create the pitch\n",
    "        pitch = Pitch(pitch_type='statsbomb', pitch_color='black', line_color='white')\n",
    "        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)\n",
    "        fig.set_facecolor(\"black\")\n",
    "        ax.set_xlim(75, 130)\n",
    "\n",
    "        for i in range(len(df_each_shoot)):\n",
    "            plt.plot((df_each_shoot.iloc[i]['X'], df_each_shoot.iloc[i]['endX']),\n",
    "                     (df_each_shoot.iloc[i]['Y'], df_each_shoot.iloc[i]['endY']),\n",
    "                     color=\"yellow\", ls='--')\n",
    "            \n",
    "            plt.scatter(df_each_shoot.iloc[i]['X'], df_each_shoot.iloc[i]['Y'], color='yellow', marker='o')\n",
    "            \n",
    "            if df_each_shoot.iloc[i]['teammate']:\n",
    "                plt.scatter(df_each_shoot.iloc[i]['location_x'], df_each_shoot.iloc[i]['location_y'], color='green')\n",
    "            else:\n",
    "                plt.scatter(df_each_shoot.iloc[i]['location_x'], df_each_shoot.iloc[i]['location_y'], color='red')\n",
    "\n",
    "        # Add dummy points for legend only\n",
    "        plt.scatter([], [], color='yellow', marker='o', label='Shooter')\n",
    "        plt.scatter([], [], color='green', marker='o', label='Attacking')\n",
    "        plt.scatter([], [], color='red', marker='o', label='Defending')\n",
    "\n",
    "        plt.title(f\"{selected_match_events['match'].iloc[0]}\\n{df_each_shoot_team} - {df_each_shoot_shooter} (Outcome: {df_each_shoot_shot_outcome})\", color='white')\n",
    "        st.pyplot(fig)\n",
    "\n",
    "    plot_shots(selected_shot)\n",
    "else:\n",
    "    st.write(\"No shots available for the selected match.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "994eeaa3-e195-40ef-a2a1-41a289b7b732",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
