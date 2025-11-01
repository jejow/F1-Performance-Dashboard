import os
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#ANNUAL_DIR = os.path.join(ROOT_DIR, "f1_annual_data")
CLEANED_DIR = os.path.join(ROOT_DIR, "f1_cleaned_data")

@st.cache_data(ttl=3600)
def load_data(year, session_type, columns=None, sample_frac=None):
    """Load complete dataset from f1_cleaned_data/<year>/<session>/*.csv"""
    folder = os.path.join(CLEANED_DIR, str(year), session_type)
    if not os.path.exists(folder):
        st.warning(f"Data not available: {folder}")
        return pd.DataFrame()

    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.csv')]
    if not files:
        return pd.DataFrame()

    dfs = []
    for path in files:
        try:
            df_part = pd.read_csv(path, usecols=columns)
            dfs.append(df_part)
        except Exception:
            try:
                df_part = pd.read_csv(path)
                if columns:
                    df_part = df_part[[c for c in columns if c in df_part.columns]]
                dfs.append(df_part)
            except Exception:
                continue

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    return df

@st.cache_data(ttl=3600)
def load_data_filtered(year, session_type, driver_name=None, circuit=None, max_rows=None):
    """Load filtered by driver/circuit at file level"""
    cleaned_dir = os.path.join(CLEANED_DIR, str(year), session_type)
    if not os.path.exists(cleaned_dir):
        return pd.DataFrame()

    files = [os.path.join(cleaned_dir, f) for f in os.listdir(cleaned_dir) if f.lower().endswith('.csv')]
    matched = []
    for fpath in files:
        try:
            head = pd.read_csv(fpath, nrows=1)
        except Exception:
            continue
        if circuit and 'race' in head.columns:
            if str(head.iloc[0].get('race', '')) != str(circuit):
                continue
        if driver_name and 'driver_name' in head.columns:
            if str(head.iloc[0].get('driver_name', '')) != str(driver_name):
                continue
        matched.append(fpath)

    if not matched:
        return pd.DataFrame()

    dfs = []
    for p in matched:
        try:
            dfs.append(pd.read_csv(p, nrows=max_rows))
        except Exception:
            continue
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

    return df

@st.cache_data(ttl=3600)
def get_data_summary(year, session_type):
    """Get drivers/circuits summary from sample files"""
    folder = os.path.join(CLEANED_DIR, str(year), session_type)
    if not os.path.exists(folder):
        return {}
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.csv')]
    files = files[:20]
    if not files:
        return {}
    dfs = []
    for p in files:
        try:
            dfs.append(pd.read_csv(p, nrows=5000, usecols=['driver_name','race']))
        except Exception:
            try:
                dfs.append(pd.read_csv(p, nrows=1000))
            except Exception:
                continue
    if not dfs:
        return {}
    df_sample = pd.concat(dfs, ignore_index=True)

    return {
        'drivers': sorted(df_sample['driver_name'].dropna().unique().tolist()) if 'driver_name' in df_sample.columns else [],
        'circuits': sorted(df_sample['race'].dropna().unique().tolist()) if 'race' in df_sample.columns else [],
        'columns': df_sample.columns.tolist(),
    }

def get_available_years():
    """Get years from f1_cleaned_data folders"""
    years = []
    if os.path.exists(CLEANED_DIR):
        for name in os.listdir(CLEANED_DIR):
            if name.isdigit():
                years.append(int(name))
    return sorted(years)

@st.cache_data(ttl=3600)
def get_available_circuits(year, session_type):
    """Get circuits from cleaned data filenames + CSV race column"""
    circuits = set()
    cleaned_dir = os.path.join(CLEANED_DIR, str(year), session_type)
    if os.path.exists(cleaned_dir):
        seen_tokens = set()
        for fname in os.listdir(cleaned_dir):
            if not fname.lower().endswith('.csv'):
                continue
            parts = fname[:-4].split('_')
            if len(parts) < 3 or not parts[0].isdigit():
                continue
            try:
                stop_idx = parts.index('Race') if 'Race' in parts else parts.index('Sprint')
            except ValueError:
                continue
            token = '_'.join(parts[1:stop_idx])
            if token in seen_tokens:
                continue
            seen_tokens.add(token)
            fpath = os.path.join(cleaned_dir, fname)
            try:
                df1 = pd.read_csv(fpath, usecols=['race'], nrows=1)
                name = str(df1.iloc[0]['race'])
                if name:
                    circuits.add(name)
                    continue
            except Exception:
                pass
            circuits.add(token.replace('_', ' '))
    return sorted(circuits)

@st.cache_data(ttl=3600)
def get_available_drivers(year, session_type):
    """Get drivers from 1st row of each CSV"""
    cleaned_dir = os.path.join(CLEANED_DIR, str(year), session_type)
    if not os.path.exists(cleaned_dir):
        return []
    names = set()
    files = [os.path.join(cleaned_dir, f) for f in os.listdir(cleaned_dir) if f.lower().endswith('.csv')]
    for fpath in files:
        try:
            df = pd.read_csv(fpath, usecols=['driver_name'], nrows=1)
            val = str(df.iloc[0]['driver_name'])
            if val:
                names.add(val)
        except Exception:
            continue
    return sorted(names)

def create_speed_distribution(df, title="Speed Distribution", max_points=10000):
    if len(df) > max_points:
        df_plot = df.sample(n=max_points, random_state=42)
    else:
        df_plot = df
    
    fig = px.histogram(df_plot, x="speed", nbins=40, 
                      color="driver_name",
                      title=title)
    return fig

def create_speed_rpm_scatter(df, title="Speed vs RPM", max_points=5000):
    if len(df) > max_points:
        df_plot = df.sample(n=max_points, random_state=42)
    else:
        df_plot = df
    
    fig = px.scatter(df_plot, x="rpm", y="speed", 
                    color="driver_name",
                    opacity=0.5,
                    title=title)
    return fig

def create_throttle_brake_map(df, title="Throttle vs Brake", max_points=5000):
    sample_size = min(len(df), max_points)
    df_sample = df.sample(sample_size, random_state=42)
    
    fig = px.scatter(df_sample, 
                    x="throttle", 
                    y="brake",
                    color="driver_name",
                    opacity=0.5,
                    title=title)
    return fig

def create_gear_distribution(df, title="Gear Distribution"):
    gear_counts = df.groupby(["driver_name", "n_gear"]).size().reset_index(name="count")
    fig = px.bar(gear_counts, 
                x="n_gear", 
                y="count", 
                color="driver_name",
                barmode="group",
                title=title)
    return fig

def create_average_speed_bar(df, by="driver_name", title="Average Speed"):
    avg_speed = df.groupby(by)["speed"].mean().reset_index()
    avg_speed = avg_speed.sort_values("speed", ascending=False)
    
    fig = px.bar(avg_speed, 
                x=by, 
                y="speed",
                color=by,
                title=title)
    return fig

def optimize_dataframe_memory(df):
    """Downcast numeric types to reduce memory"""
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df