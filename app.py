import streamlit as st
from calculations import *

# main
df_jump_goals = get_jump_goals()
df_spike_height = get_highest_jumps()
graph_latest = graph_jump_progress(df_spike_height=df_spike_height, df_jump_goals=df_jump_goals)
latest_spike_height = get_latest_spike_height(df_spike_height=df_spike_height)
df_differences = get_differences_from_goals(latest_spike_height=latest_spike_height, df_jump_goals=df_jump_goals)
months_to_next_goal = get_months_to_next_goal(df_differences=df_differences)

# sample output to user
st.write(f"Your highest reach is now {latest_spike_height} cm")

for row in df_differences.loc[df_differences["achieved"] == 1].itertuples():
    st.write(f"You have already achieved your goal: {row[1]}!")

for row in df_differences.loc[df_differences["achieved"] == 0].itertuples():
    st.write(f"You are {round(row[4], 2)} {row[3]} away from your goal: {row[1]} ({row[2]} {row[3]})")

st.write(
    f"If you keep it up, you are about {round(months_to_next_goal['months to goal'], 2)} months away from your next goal: {months_to_next_goal['jump goal measurements']}.")

st.write(df_jump_goals)
st.plotly_chart(graph_latest)