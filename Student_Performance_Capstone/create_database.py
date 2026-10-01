from utils.data_processing import load_data
from utils.database import create_database
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="data/student_performance_data.csv", help="CSV path to create DB from")
    args = parser.parse_args()
    df = load_data(args.path)
    create_database(df)
    print("Database created at database/student_performance.db from:", args.path)
