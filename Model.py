import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
CSV_PATH = "IoT_Intrusion.csv"
MODEL_OUT = "iot_scanner_model.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.20
COLUMN_LIST = [
"flow_duration","Header_Length","Protocol Type","Duration","Rate","Srate","Drate",
"fin_flag_number","syn_flag_number","rst_flag_number","psh_flag_number","ack_flag_number",
"ece_flag_number","cwr_flag_number","ack_count","syn_count","fin_count","urg_count","rst_count",
"HTTP","HTTPS","DNS","Telnet","SMTP","SSH","IRC","TCP","UDP","DHCP","ARP","ICMP","IPv","LLC",
"Tot sum","Min","Max","AVG","Std","Tot size","IAT","Number","Magnitue","Radius","Covariance","Variance","Weight","label"
]
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV not found at {CSV_PATH}. Put your CSV file there or change CSV_PATH.")

df = pd.read_csv(CSV_PATH)
print("Loaded dataset:", df.shape)

missing = [c for c in COLUMN_LIST if c not in df.columns]
if missing:
    print("Warning: These expected columns are missing from the CSV:", missing)


use_cols = [c for c in COLUMN_LIST if c in df.columns]
print("Using columns:", len(use_cols))
df = df[use_cols].copy()
df = df.fillna(0)

if 'Protocol Type' in df.columns:
    if df['Protocol Type'].dtype == object:
        le_proto = LabelEncoder()
        df['Protocol Type'] = le_proto.fit_transform(df['Protocol Type'].astype(str))


categorical_candidates = ['Header_Length']

for c in df.columns:
    if df[c].dtype == object and c != 'label':
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c].astype(str))

if 'label' not in df.columns:
    raise KeyError("Target column 'label' not found in CSV.")
X = df.drop(columns=['label'])
y = df['label']

if y.dtype == object:
    le_y = LabelEncoder()
    y = le_y.fit_transform(y.astype(str))

print("Feature matrix shape:", X.shape)
print("Target distribution:\n", pd.Series(y).value_counts())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
model = RandomForestClassifier(
    n_estimators=200,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    class_weight='balanced'
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, zero_division=0)
cm = confusion_matrix(y_test, y_pred)

print("Accuracy:", acc)
print(report)
print("Confusion matrix:\n", cm)

out_dir="Training_output"
os.makedirs(out_dir, exist_ok=True)
pd.DataFrame(cm).to_csv(os.path.join(out_dir, "confusion_matrix.csv"), index=False)
with open(os.path.join(out_dir, "classification_report.txt"), "w") as f:
    f.write(report)

pd.DataFrame({"accuracy": [acc]}).to_csv(os.path.join(out_dir, "accuracy.csv"), index=False)


joblib.dump(model, MODEL_OUT)
print(f"Trained model saved to: {MODEL_OUT}")
if hasattr(model,"feature_importances_"):
    fi=pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
        }).sort_values("importance", ascending=False)
    fi.to_csv(os.path.join(out_dir, "feature_importances.csv"), index=False)
    print("Top features:\n", fi.head(10))