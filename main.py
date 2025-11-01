import streamlit as st
import plotly.express as px
from utils import *

st.set_page_config(
    page_title="F1 Performance Overview",
    page_icon="🏎️",
    layout="wide"
)

st.sidebar.header("F1 Data Control Panel")
year = st.sidebar.selectbox("Select Year", get_available_years())
session_type = st.sidebar.radio("Session Type", ["race", "sprint"])

df = load_data(year, session_type)

if df.empty:
    st.error("❌ No data available")
    st.stop()

all_drivers = get_available_drivers(year, session_type)
selected_driver = st.sidebar.selectbox("Select Driver (optional)", ["All"] + all_drivers)

if selected_driver != "All":
    df = df[df['driver_name'] == selected_driver]

st.title(f"🏎️ F1 {year} {session_type.capitalize()} Performance Overview")

col1, col2, col3 = st.columns(3)
with col1:
    if 'race' in df.columns:
        n_races = df['race'].nunique()
        st.metric("Total Races/Sprints", f"{n_races:,}")
    else:
        st.metric("Total Sessions", "1")

with col2:
    n_drivers = df['driver_name'].nunique()
    st.metric("Total Drivers", f"{n_drivers:,}")

with col3:
    n_datapoints = len(df)
    st.metric("Total Data Points", f"{n_datapoints:,}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Average Speed per Driver")
    fig = create_average_speed_bar(df)
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader("⚙️ Average RPM per Driver")
    avg_rpm = df.groupby('driver_name')['rpm'].mean().reset_index()
    fig = px.bar(avg_rpm,
                x='driver_name',
                y='rpm',
                color='driver_name',
                title="Average RPM per Driver")
    st.plotly_chart(fig, width='stretch')

st.subheader("🏁 Top Speed per Race")
if 'race' in df.columns:
    top_speeds = df.groupby(['race', 'driver_name'])['speed'].max().reset_index()
    fig = px.bar(top_speeds, 
                x='race', 
                y='speed', 
                color='driver_name',
                title="Top Speed per Race",
                barmode='group')
    st.plotly_chart(fig, width='stretch')
else:
    st.info("Race information not available")

st.subheader("⏱️ Throttle & Brake Usage")
col1, col2 = st.columns(2)

with col1:
    avg_throttle = df.groupby('driver_name')['throttle'].mean().reset_index()
    fig = px.bar(avg_throttle, 
                x='driver_name', 
                y='throttle',
                title="Average Throttle Usage per Driver",
                color='driver_name')
    st.plotly_chart(fig, width='stretch')

with col2:
    avg_brake = df.groupby('driver_name')['brake'].mean().reset_index()
    fig = px.bar(avg_brake, 
                x='driver_name', 
                y='brake',
                title="Average Brake Usage per Driver",
                color='driver_name')
    st.plotly_chart(fig, width='stretch')