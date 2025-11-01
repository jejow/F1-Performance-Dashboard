import streamlit as st
import time
import pandas as pd


class PerformanceMonitor:
    """Simple performance monitoring for Streamlit apps."""
    
    def __init__(self):
        self.start_time = time.time()
        self.checkpoints = {}
    
    def checkpoint(self, name):
        elapsed = time.time() - self.start_time
        self.checkpoints[name] = elapsed
        return elapsed
    
    def display_sidebar(self, df=None):
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚡ Performance")
        
        total_time = time.time() - self.start_time
        st.sidebar.metric("Total Load Time", f"{total_time:.2f}s")
        
        if df is not None and not df.empty:
            st.sidebar.metric("Data Points", f"{len(df):,}")
            memory_mb = df.memory_usage(deep=True).sum() / 1024**2
            st.sidebar.metric("Memory Usage", f"{memory_mb:.1f} MB")
        
        if self.checkpoints:
            with st.sidebar.expander("📊 Checkpoints"):
                for name, elapsed in self.checkpoints.items():
                    st.write(f"**{name}:** {elapsed:.2f}s")


def add_performance_metrics(df=None):
    """
    Quick helper to add performance metrics to sidebar.
    
    Usage:
        from performance_monitor import add_performance_metrics
        
        # At start of page
        perf = add_performance_metrics()
        
        # After loading data
        df = load_data(2023, 'race')
        perf.checkpoint("Data Loaded")
        
        # At end of page
        perf.display_sidebar(df)
    """
    if 'perf_monitor' not in st.session_state:
        st.session_state.perf_monitor = PerformanceMonitor()
    
    return st.session_state.perf_monitor

def show_perf_metrics_inline(df):
    """
    Inline version - just copy this to bottom of any page:
    
    # At end of page
    show_perf_metrics_inline(df)
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ Performance")
    
    if df is not None and not df.empty:
        st.sidebar.metric("Data Points", f"{len(df):,}")
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.sidebar.metric("Memory Usage", f"{memory_mb:.1f} MB")

        original_rows = len(df)
        if 'sample_info' in st.session_state:
            sample_info = st.session_state.sample_info
            original_rows = sample_info.get('original_rows', len(df))
            st.sidebar.info(f"🎯 Using {len(df):,} / {original_rows:,} rows")
