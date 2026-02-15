import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train(csv_file):
    df = pd.read_csv(csv_file)

    X = df[["days_absent","missed_topics","avg_marks","difficulty_score"]]
    y = df["risk_level"]

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, "model.pkl")
    print("Model trained successfully!")

if __name__ == "__main__":
    train("students.csv")  # your dataset file
