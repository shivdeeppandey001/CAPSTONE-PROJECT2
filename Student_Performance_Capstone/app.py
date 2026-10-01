import streamlit as st
import plotly.express as px
import pandas as pd
import os
import subprocess
import sys
from utils.data_processing import load_data
from utils.risk_engine import add_risk_analysis
from utils.recommendations import generate_recommendations
from utils.database import create_database

st.set_page_config(page_title="Student Performance Dashboard", page_icon="🎓", layout="wide")

@st.cache_data
def load_and_prepare(path: str):
    df = load_data(path)
    df = add_risk_analysis(df)
    return df

from pathlib import Path

# Resolve project root and data directory reliably
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# Dataset selector using files under project data dir
data_files = sorted([f.name for f in DATA_DIR.iterdir() if f.is_file() and f.suffix.lower() == '.csv'])
if not data_files:
    st.warning("No CSV files found in data/. Upload a dataset using the sidebar.")
    selected = st.sidebar.text_input("Enter dataset filename to create (will be saved to data/)")
else:
    selected = st.sidebar.selectbox("Dataset", data_files, index=0)

# persist selection so other pages can read it from session_state
st.session_state['dataset'] = selected

# Upload new dataset
uploaded_file = st.sidebar.file_uploader("Upload CSV dataset", type=["csv"])
if uploaded_file is not None:
    save_path = DATA_DIR / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"Saved uploaded dataset to data/{uploaded_file.name}")
    # update selection
    data_files = sorted([f.name for f in DATA_DIR.iterdir() if f.is_file() and f.suffix.lower() == '.csv'])
    selected = uploaded_file.name

data_path = DATA_DIR / selected
df = load_and_prepare(str(data_path))

st.title("🎓 Student Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(df))
col2.metric("Average Marks", f"{df['Marks'].mean():.1f}")
col3.metric("Average Attendance (%)", f"{df['Attendance(%)'].mean():.1f}")
col4.metric("Average Logins", f"{df['Logins'].mean():.1f}")

with st.expander("Filters"):
    status_filter = st.multiselect("Status", options=sorted(df['Status'].unique()), default=list(df['Status'].unique()))
    min_mark, max_mark = st.slider("Marks range", 0, 100, (0, 100))
    df = df[df['Status'].isin(status_filter)]
    df = df[(df['Marks'] >= min_mark) & (df['Marks'] <= max_mark)]

# Actions: create DB or train model
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Create SQLite DB from selected dataset"):
        create_database(load_data(data_path))
        st.success("Database created/updated from selected dataset.")
with col_b:
    if st.button("Train model on selected dataset (background)"):
        # spawn background process using same Python interpreter
        subprocess.Popen([sys.executable, "train_model.py", data_path])
        st.info("Training started in background. Check terminal for progress.")

# Status distribution
fig = px.pie(df, names='Status', title='Student Status Distribution', hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# Marks distribution
fig2 = px.histogram(df, x='Marks', nbins=10, title='Marks Distribution')
st.plotly_chart(fig2, use_container_width=True)

# Attendance vs Marks
fig3 = px.scatter(df, x='Attendance(%)', y='Marks', color='Status', size='Logins', title='Attendance vs Marks')
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Students Table")
st.table(df.reset_index(drop=True))

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, file_name='student_performance_report.csv', mime='text/csv')
