import streamlit as st
import plotly.express as px
from pathlib import Path
from utils.data_processing import load_data
from utils.risk_engine import add_risk_analysis

st.set_page_config(page_title="Risk Analysis", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
if not DATA_DIR.exists():
	DATA_DIR.mkdir(parents=True, exist_ok=True)

# Select dataset from session_state (set by main app) or fallback to first CSV
data_files = sorted([f.name for f in DATA_DIR.iterdir() if f.is_file() and f.suffix.lower() == '.csv'])
dataset = st.session_state.get('dataset') if 'dataset' in st.session_state else None
if dataset not in data_files:
	if data_files:
		dataset = st.selectbox("Select dataset", data_files, index=0)
	else:
		st.warning("No datasets found in data/. Upload one in the main page.")
		dataset = None

df = add_risk_analysis(load_data(str(DATA_DIR / dataset)))

st.title("⚠️ Risk Analysis")
st.markdown("This page identifies students who may require additional academic or engagement support.")

# KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(df))
col2.metric("Average Marks", f"{df['Marks'].mean():.1f}")
col3.metric("Average Attendance (%)", f"{df['Attendance(%)'].mean():.1f}")
col4.metric("Average Logins", f"{df['Logins'].mean():.1f}")

# Distribution charts
left, right = st.columns(2)
with left:
	fig = px.pie(df, names='RiskLevel', title='Risk Level Distribution', hole=0.4)
	st.plotly_chart(fig, use_container_width=True)
with right:
	fig2 = px.pie(df, names='Status', title='Status Distribution', hole=0.4)
	st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Filters for detailed view
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
	risk_options = ["All"] + sorted(df['RiskLevel'].unique().tolist())
	risk_filter = st.selectbox("Risk Level", risk_options, index=0)
with filter_col2:
	status_filter = st.multiselect("Status", options=sorted(df['Status'].unique()), default=list(df['Status'].unique()))

filtered = df.copy()
if risk_filter != "All":
	filtered = filtered[filtered['RiskLevel'] == risk_filter]
if status_filter:
	filtered = filtered[filtered['Status'].isin(status_filter)]

st.subheader(f"Students — {len(filtered)} matching")

# Show top and bottom performers in the filtered set
perf_col1, perf_col2 = st.columns(2)
with perf_col1:
	st.markdown("**Top performers (by Marks)**")
	topn = filtered.sort_values('Marks', ascending=False).head(5)[['StudentID','Name','Marks','Attendance(%)','Logins','Status','RiskLevel']]
	st.table(topn)
with perf_col2:
	st.markdown("**Lowest performers (by Marks)**")
	botn = filtered.sort_values('Marks', ascending=True).head(5)[['StudentID','Name','Marks','Attendance(%)','Logins','Status','RiskLevel']]
	st.table(botn)

st.markdown("---")

cols = ['StudentID','Name','Marks','Attendance(%)','Logins','Status','RiskScore','RiskLevel']
st.table(filtered[cols].reset_index(drop=True))

# Download filtered data
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download filtered students (CSV)", csv, file_name='filtered_students.csv', mime='text/csv')
