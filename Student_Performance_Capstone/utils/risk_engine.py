from typing import Any

def calculate_risk_score(row: Any, max_logins: int) -> float:
    marks = row.get("Marks", 0) or 0
    attendance = row.get("Attendance(%)", 0) or 0
    logins = row.get("Logins", 0) or 0
    marks_score = marks / 100
    attendance_score = attendance / 100
    engagement_score = (logins / max_logins) if max_logins > 0 else 0
    risk_score = (
        (1 - marks_score) * 0.50
        + (1 - attendance_score) * 0.30
        + (1 - engagement_score) * 0.20
    ) * 100
    return round(risk_score, 2)

def assign_risk_level(score: float) -> str:
    if score < 30:
        return "Low Risk"
    if score < 60:
        return "Moderate Risk"
    return "High Risk"

def add_risk_analysis(df):
    if "Logins" in df.columns and df["Logins"].notna().any():
        max_logins = int(df["Logins"].max())
    else:
        max_logins = 0
    df = df.copy()
    df["RiskScore"] = df.apply(lambda r: calculate_risk_score(r, max_logins), axis=1)
    df["RiskLevel"] = df["RiskScore"].apply(assign_risk_level)
    return df
