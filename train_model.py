import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle, os

df = pd.read_csv("data/pothole_data.csv")
X = df.drop("severity", axis=1)
y = df["severity"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

os.makedirs("model", exist_ok=True)
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)
print("model.pkl saved!")