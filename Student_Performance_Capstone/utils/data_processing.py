import pandas as pd

def load_data(path: str = "data/student_performance_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(how="all")
    df = df.drop_duplicates()
    df.columns = df.columns.str.strip()
    # Convert numeric columns
    for col in ["Marks", "Attendance(%)", "Logins"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Ensure required columns exist
    if "StudentID" not in df.columns and "ID" in df.columns:
        df = df.rename(columns={"ID": "StudentID"})
    df = df.dropna(subset=["StudentID", "Name"]) 
    return df
