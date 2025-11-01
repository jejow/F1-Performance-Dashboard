import streamlit as st
import plotly.express as px
from utils import *

st.set_page_config(
    page_title="Circuit Analysis",
    page_icon="🏎️",
    layout="wide"
)

st.sidebar.header("Circuit Analysis Controls")
year = st.sidebar.selectbox("Select Year", get_available_years())
session_type = st.sidebar.radio("Session Type", ["race", "sprint"])

circuits = get_available_circuits(year, session_type)
if not circuits:
    st.error("❌ Circuit information not available")
    st.stop()

selected_circuit = st.sidebar.selectbox("Select Circuit", circuits)

df_circuit = load_data_filtered(year, session_type, circuit=selected_circuit)

if df_circuit.empty:
    st.error("❌ No data available for this circuit")
    st.stop()

st.title(f"🧩 Circuit Analysis: {selected_circuit}")

st.subheader("📊 Speed Distribution")
fig = px.histogram(df_circuit,
                  x="speed",
                  color="driver_name",
                  nbins=50,
                  title=f"Speed Distribution at {selected_circuit}")
st.plotly_chart(fig, width='stretch')

st.subheader("⚙️ Gear vs Speed Analysis")
col1, col2 = st.columns(2)

with col1:
    avg_speed_gear = df_circuit.groupby(['driver_name', 'n_gear'])['speed'].mean().reset_index()
    fig = px.line(avg_speed_gear,
                  x='n_gear',
                  y='speed',
                  color='driver_name',
                  title="Average Speed per Gear",
                  labels={'n_gear': 'Gear', 'speed': 'Speed (km/h)'})
    st.plotly_chart(fig, width='stretch')

with col2:
    gear_dist = df_circuit.groupby(['driver_name', 'n_gear']).size().reset_index(name='count')
    fig = px.bar(gear_dist,
                 x='n_gear',
                 y='count',
                 color='driver_name',
                 title="Gear Usage Distribution",
                 labels={'n_gear': 'Gear', 'count': 'Frequency'})
    st.plotly_chart(fig, width='stretch')

st.subheader("🔄 RPM vs Throttle Pattern")
fig = px.scatter(df_circuit.sample(min(len(df_circuit), 5000)),
                x="rpm",
                y="throttle",
                color="driver_name",
                opacity=0.6,
                title="RPM vs Throttle Pattern")
st.plotly_chart(fig, width='stretch')

st.subheader("📊 Circuit Performance Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    avg_speed = df_circuit.groupby('driver_name')['speed'].mean().reset_index()
    fig = px.bar(avg_speed.sort_values('speed', ascending=False),
                 x='driver_name',
                 y='speed',
                 title="Average Speed per Driver",
                 color='driver_name')
    st.plotly_chart(fig, width='stretch')

with col2:
    avg_throttle = df_circuit.groupby('driver_name')['throttle'].mean().reset_index()
    fig = px.bar(avg_throttle.sort_values('throttle', ascending=False),
                 x='driver_name',
                 y='throttle',
                 title="Average Throttle Usage",
                 color='driver_name')
    st.plotly_chart(fig, width='stretch')

with col3:
    avg_brake = df_circuit.groupby('driver_name')['brake'].mean().reset_index()
    fig = px.bar(avg_brake.sort_values('brake', ascending=False),
                 x='driver_name',
                 y='brake',
                 title="Average Brake Usage",
                 color='driver_name')
    st.plotly_chart(fig, width='stretch')

st.subheader("💡 Circuit Insights")

avg_speed = df_circuit['speed'].mean()
max_speed = df_circuit['speed'].max()
avg_gear = df_circuit['n_gear'].mean()
most_used_gear = df_circuit['n_gear'].mode().iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Speed", f"{avg_speed:.1f} km/h")

with col2:
    st.metric("Maximum Speed", f"{max_speed:.1f} km/h")

with col3:
    st.metric("Average Gear", f"{avg_gear:.1f}")

with col4:
    st.metric("Most Used Gear", f"{most_used_gear}")

characteristics = []

if avg_speed > 200:
    characteristics.append("High-speed circuit")
elif avg_speed < 150:
    characteristics.append("Technical circuit")
else:
    characteristics.append("Balanced circuit")

if df_circuit['brake'].mean() > 30:
    characteristics.append("Heavy braking zones")

if df_circuit['n_gear'].nunique() > 6:
    characteristics.append("Various gear combinations")

st.info("Circuit Characteristics: " + ", ".join(characteristics))