def generate_recommendations(row) -> str:
    recs = []
    marks = row.get("Marks", 0) or 0
    attendance = row.get("Attendance(%)", 0) or 0
    logins = row.get("Logins", 0) or 0
    if marks < 50:
        recs.append("Provide additional academic support.")
    elif marks < 60:
        recs.append("Encourage additional revision and practice.")
    else:
        recs.append("Maintain current academic performance.")
    if attendance < 60:
        recs.append("Attendance needs immediate improvement.")
    elif attendance < 75:
        recs.append("Encourage more regular attendance.")
    else:
        recs.append("Attendance is satisfactory.")
    if logins < 15:
        recs.append("Encourage regular LMS/platform engagement.")
    return "; ".join(recs)
