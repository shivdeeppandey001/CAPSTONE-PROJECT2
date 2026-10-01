import streamlit as st
import joblib
import numpy as np
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="ML Prediction", layout="wide")
st.title("🤖 Student Status Prediction")

try:
    model = joblib.load("models/model.pkl")
    le = joblib.load("models/label_encoder.pkl")
except Exception:
    st.warning("No trained model found. Run `python train_model.py` first.")
    model = None
    le = None

st.subheader("Single prediction")
marks = st.slider("Marks", 0, 100, 70, key="marks")
attendance = st.slider("Attendance (%)", 0, 100, 75, key="attendance")
logins = st.number_input("Logins", min_value=0, value=10, key="logins")

if st.button("Predict Single"):
    if model is None or le is None:
        st.error("Model unavailable. Train model first.")
    else:
        X = np.array([[marks, attendance, logins]])
        pred = model.predict(X)[0]
        label = le.inverse_transform([pred])[0]
        probs = model.predict_proba(X)[0]
        # map probs to labels order
        labels = le.inverse_transform(np.arange(len(le.classes_)))
        prob_map = dict(zip(labels, probs))
        st.success(f"Predicted Status: {label}")
        st.write("Probabilities:")
        st.json({k: float(round(v, 4)) for k, v in prob_map.items()})

st.markdown("---")
st.subheader("Batch prediction from CSV")
uploaded = st.file_uploader("Upload CSV with columns: Marks, Attendance(%), Logins", type=["csv"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        df = None

    if df is not None:
        required = ["Marks", "Attendance(%)", "Logins"]
        if not all(col in df.columns for col in required):
            st.error(f"CSV must contain these columns: {required}")
        elif model is None or le is None:
            st.error("Model unavailable. Train model first.")
        else:
            X = df[required].fillna(0).values
            preds = model.predict(X)
            probs = model.predict_proba(X)
            pred_labels = le.inverse_transform(preds)
            df["PredictedStatus"] = pred_labels
            # attach probability for predicted class
            df["PredictedProb"] = [float(round(p.max(), 4)) for p in probs]
            st.success("Batch prediction completed")
            st.table(df.head(200))
            towrite = BytesIO()
            df.to_csv(towrite, index=False)
            towrite.seek(0)
            st.download_button("Download predictions CSV", towrite, file_name="predictions.csv", mime="text/csv")

