import streamlit as st
from pathlib import Path
from utils.data_processing import load_data
from utils.risk_engine import add_risk_analysis
from utils.recommendations import generate_recommendations

st.set_page_config(page_title="Student Details", layout="wide")

# Determine dataset to use: prefer session_state value set in main app, else list data files
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
if not DATA_DIR.exists():
	DATA_DIR.mkdir(parents=True, exist_ok=True)

data_files = sorted([f.name for f in DATA_DIR.iterdir() if f.is_file() and f.suffix.lower() == '.csv'])
dataset = st.session_state.get('dataset') if 'dataset' in st.session_state else None
if dataset not in data_files:
	if data_files:
		dataset = st.selectbox("Select dataset", data_files, index=0)
	else:
		st.warning("No datasets found in data/. Upload one in the main page.")
		dataset = None
else:
	st.write(f"Using dataset: {dataset}")

df = add_risk_analysis(load_data(str(DATA_DIR / dataset)))

st.title("👨‍🎓 Student Performance Details")
search = st.text_input("Search student by name (partial)")
names = df['Name'].sort_values().unique()
if search:
	names = [n for n in names if search.lower() in n.lower()]
student = st.selectbox("Select student", names)
row = df[df['Name'] == student].iloc[0]
st.metric("Marks", f"{row['Marks']}/100")
st.metric("Attendance(%)", f"{row['Attendance(%)']}%")
st.metric("Logins", int(row['Logins']))
st.metric("Risk Score", f"{row['RiskScore']} ({row['RiskLevel']})")
st.subheader("Recommendations")
st.write(generate_recommendations(row))
