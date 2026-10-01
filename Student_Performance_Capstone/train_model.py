import joblib
import pandas as pd
import argparse
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from utils.data_processing import load_data


def train_and_save(path: str = "data/student_performance_data.csv"):
    df = load_data(path)
    df = load_data()
    features = ["Marks", "Attendance(%)", "Logins"]
    df = df.dropna(subset=features + ["Status"]).copy()
    X = df[features]
    y = df["Status"]
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.25, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    joblib.dump(le, "models/label_encoder.pkl")
    joblib.dump(le, "models/label_encoder.pkl")
    print("Model and label encoder saved to models/")
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="data/student_performance_data.csv", help="CSV path to train on")
    args = parser.parse_args()
    train_and_save(args.path)
    train_and_save()
