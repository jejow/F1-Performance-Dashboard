import streamlit as st
import plotly.express as px
import pandas as pd
from utils import *

st.set_page_config(
    page_title="Race vs Sprint Comparison",
    page_icon="🏎️",
    layout="wide"
)

st.title("📅 Race vs Sprint Comparison (2023-2025)")

@st.cache_data(ttl=3600)
def load_comparison_data():
    comparison_data = []
    
    for year in [2023, 2024, 2025]:
        for session_type in ['race', 'sprint']:
            df = load_data(year, session_type, 
                          columns=['speed', 'rpm', 'driver_name'])
            if not df.empty:
                comparison_data.append({
                    'year': year,
                    'session_type': session_type,
                    'avg_speed': df['speed'].mean(),
                    'max_speed': df['speed'].max(),
                    'avg_rpm': df['rpm'].mean(),
                    'data_points': len(df),
                    'n_drivers': df['driver_name'].nunique()
                })
    
    return pd.DataFrame(comparison_data)

comp_df = load_comparison_data()

if comp_df.empty:
    st.error("❌ No comparison data available")
    st.stop()

st.subheader("📈 Average Speed Evolution")
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(comp_df,
                x='year',
                y='avg_speed',
                color='session_type',
                barmode='group',
                title="Average Speed: Race vs Sprint",
                labels={'avg_speed': 'Average Speed (km/h)'})
    st.plotly_chart(fig, width='stretch')

with col2:
    fig = px.bar(comp_df,
                x='year',
                y='max_speed',
                color='session_type',
                barmode='group',
                title="Maximum Speed: Race vs Sprint",
                labels={'max_speed': 'Maximum Speed (km/h)'})
    st.plotly_chart(fig, width='stretch')

st.subheader("📊 Session Data Volume")
fig = px.bar(comp_df,
            x='year',
            y='data_points',
            color='session_type',
            barmode='group',
            title="Total Data Points per Session Type",
            labels={'data_points': 'Number of Data Points'})
st.plotly_chart(fig, width='stretch')

st.subheader("📉 Average RPM Evolution")
fig = px.line(comp_df,
             x='year',
             y='avg_rpm',
             color='session_type',
             markers=True,
             title="Average RPM Evolution (2023-2025)",
             labels={'avg_rpm': 'Average RPM'})
st.plotly_chart(fig, width='stretch')

st.subheader("🏎️ Driver Performance Evolution")

available_drivers_sample = get_available_drivers(2023, 'race')
if not available_drivers_sample:
    st.warning("No driver data available")
    st.stop()

selected_driver = st.selectbox("Select Driver for Analysis", available_drivers_sample)

driver_data = []
for year in [2023, 2024, 2025]:
    for session_type in ['race', 'sprint']:
        driver_df = load_data_filtered(year, session_type, driver_name=selected_driver)
        if not driver_df.empty:
            driver_data.append({
                'year': year,
                'session_type': session_type,
                'avg_speed': driver_df['speed'].mean(),
                'avg_throttle': driver_df['throttle'].mean(),
                'avg_brake': driver_df['brake'].mean()
            })

driver_comp_df = pd.DataFrame(driver_data)

if not driver_comp_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(driver_comp_df,
                     x='year',
                     y='avg_speed',
                     color='session_type',
                     markers=True,
                     title=f"{selected_driver}'s Average Speed Evolution",
                     labels={'avg_speed': 'Average Speed (km/h)'})
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.line(driver_comp_df,
                     x='year',
                     y='avg_throttle',
                     color='session_type',
                     markers=True,
                     title=f"{selected_driver}'s Throttle Usage Evolution",
                     labels={'avg_throttle': 'Average Throttle %'})
        st.plotly_chart(fig, width='stretch')