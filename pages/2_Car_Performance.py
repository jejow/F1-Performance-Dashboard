import streamlit as st
import plotly.express as px
from utils import *

st.set_page_config(
    page_title="Car Performance Analysis",
    page_icon="🏎️",
    layout="wide"
)

st.sidebar.header("Car Performance Controls")
year = st.sidebar.selectbox("Select Year", get_available_years())
session_type = st.sidebar.radio("Session Type", ["race", "sprint"])

needed_columns = ['driver_name', 'speed', 'rpm', 'n_gear', 'throttle', 'brake']
df = load_data(year, session_type, columns=needed_columns)

if df.empty:
    st.error("❌ No data available")
    st.stop()

st.title(f"🧱 Car Performance Analysis - {year} {session_type.capitalize()}")

st.subheader("📊 Engine RPM vs Speed Efficiency")
fig = px.scatter(df, 
                x="rpm", 
                y="speed",
                color="driver_name",
                title="Engine Efficiency Curve",
                labels={"rpm": "Engine RPM", "speed": "Speed (km/h)"})
st.plotly_chart(fig, width='stretch')

st.subheader("⚙️ Gear Shift Patterns")
col1, col2 = st.columns(2)

with col1:
    avg_speed_gear = df.groupby(['driver_name', 'n_gear'])['speed'].mean().reset_index()
    fig = px.line(avg_speed_gear,
                  x='n_gear',
                  y='speed',
                  color='driver_name',
                  title="Average Speed per Gear",
                  labels={'n_gear': 'Gear', 'speed': 'Average Speed (km/h)'})
    st.plotly_chart(fig, width='stretch')

with col2:
    gear_dist = df.groupby(['driver_name', 'n_gear']).size().reset_index(name='count')
    fig = px.bar(gear_dist,
                 x='n_gear',
                 y='count',
                 color='driver_name',
                 title="Gear Usage Distribution",
                 labels={'n_gear': 'Gear', 'count': 'Frequency'})
    st.plotly_chart(fig, width='stretch')

st.subheader("🏎️ Top Speed Analysis")
top_speeds = df.groupby('driver_name')['speed'].max().reset_index()
top_speeds = top_speeds.sort_values('speed', ascending=False)

fig = px.bar(top_speeds,
             x='driver_name',
             y='speed',
             color='driver_name',
             title="Maximum Speed Achieved",
             labels={'speed': 'Top Speed (km/h)', 'driver_name': 'Driver'})
st.plotly_chart(fig, width='stretch')

st.subheader("🚀 Acceleration Analysis")
col1, col2 = st.columns(2)

with col1:
    avg_speed_throttle = df.groupby('throttle').agg({
        'speed': 'mean',
        'driver_name': 'first'
    }).reset_index()
    
    fig = px.scatter(avg_speed_throttle,
                    x='throttle',
                    y='speed',
                    title="Speed vs Throttle Response",
                    labels={'throttle': 'Throttle %', 'speed': 'Speed (km/h)'})
    st.plotly_chart(fig, width='stretch')

with col2:
    fig = px.histogram(df,
                      x='rpm',
                      color='driver_name',
                      title="Engine RPM Distribution",
                      labels={'rpm': 'Engine RPM'})
    st.plotly_chart(fig, width='stretch')

st.subheader("📊 Key Performance Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_speed = df['speed'].mean()
    st.metric("Average Speed", f"{avg_speed:.1f} km/h")

with col2:
    max_speed = df['speed'].max()
    st.metric("Maximum Speed", f"{max_speed:.1f} km/h")

with col3:
    avg_rpm = df['rpm'].mean()
    st.metric("Average RPM", f"{avg_rpm:.0f}")

with col4:
    max_rpm = df['rpm'].max()
    st.metric("Maximum RPM", f"{max_rpm:.0f}")