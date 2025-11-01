import streamlit as st
import plotly.express as px
from utils import *

st.set_page_config(
    page_title="Driver Performance Analysis",
    page_icon="🏎️",
    layout="wide"
)

st.sidebar.header("Driver Analysis Controls")
year = st.sidebar.selectbox("Choose Year", get_available_years())
session_type = st.sidebar.radio("Session Type", ["race", "sprint"])

available_drivers = get_available_drivers(year, session_type)
if not available_drivers:
    st.error("❌ No data available")
    st.stop()

selected_driver = st.sidebar.selectbox("Select Driver", available_drivers)

df_driver = load_data_filtered(year, session_type, driver_name=selected_driver)

if df_driver.empty:
    st.error("❌ No data available for this driver")
    st.stop()

st.title(f"⚙️ {selected_driver}'s Performance - {year} {session_type.capitalize()}")

col1, col2 = st.columns([3, 1])
with col2:
    st.info(f"📊 {len(df_driver):,} data points")

st.divider()

st.subheader("📊 Speed vs RPM Analysis")
fig = create_speed_rpm_scatter(df_driver)
st.plotly_chart(fig, width='stretch')

st.subheader("🦶 Throttle vs Brake Analysis")
fig = create_throttle_brake_map(df_driver)
st.plotly_chart(fig, width='stretch')

st.subheader("⚙️ Gear Usage Distribution")
fig = create_gear_distribution(df_driver)
st.plotly_chart(fig, width='stretch')

if 'race' in df_driver.columns:
    st.subheader("🧭 Average Speed per Circuit")
    avg_speed_circuit = df_driver.groupby('race')['speed'].mean().reset_index()
    avg_speed_circuit = avg_speed_circuit.sort_values('speed', ascending=False)

    fig = px.bar(avg_speed_circuit,
                x='race',
                y='speed',
                title=f"Average Speed per Circuit - {selected_driver}",
                color='speed',
                color_continuous_scale='Viridis')
    st.plotly_chart(fig, width='stretch')

st.subheader("📉 Speed Over Time")

col1, col2 = st.columns([4, 1])
with col2:
    if len(df_driver) > 2000:
        show_sampled = st.checkbox("Use sampling", value=False, 
                                   help="Sampling prevents browser freeze")
    else:
        show_sampled = True

if 'lap' in df_driver.columns:
    avg_speed_lap = df_driver.groupby('lap')['speed'].mean().reset_index()
    fig = px.line(avg_speed_lap,
                 x='lap',
                 y='speed',
                 title=f"Average Speed per Lap - {selected_driver}")
    st.plotly_chart(fig, width='stretch')
else:
    if 'date' in df_driver.columns:
        df_sorted = df_driver.sort_values('date')
        
        if show_sampled and len(df_sorted) > 2000:
            max_points = 2000
            step = len(df_sorted) // max_points
            df_plot = df_sorted.iloc[::step]
            title_suffix = f" (showing {len(df_plot):,} of {len(df_sorted):,} points)"
        else:
            df_plot = df_sorted
            title_suffix = ""
        
        fig = px.line(df_plot,
                     x='date',
                     y='speed',
                     title=f"Speed Over Time - {selected_driver}{title_suffix}")
        st.plotly_chart(fig, width='stretch')
        
        if not show_sampled and len(df_sorted) > 5000:
            st.warning("⚠️ Large dataset may be slow. Consider enabling sampling.")
            st.warning("⚠️ Large dataset may be slow. Consider enabling sampling.")

st.subheader("🎯 Driving Style Insights")
col1, col2, col3 = st.columns(3)

with col1:
    avg_throttle = df_driver['throttle'].mean()
    st.metric("Average Throttle", f"{avg_throttle:.1f}%")

with col2:
    avg_brake = df_driver['brake'].mean()
    st.metric("Average Brake", f"{avg_brake:.1f}%")

with col3:
    avg_speed = df_driver['speed'].mean()
    st.metric("Average Speed", f"{avg_speed:.1f} km/h")
