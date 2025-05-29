import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load dataset
column_names = [f'feature_{i}' for i in range(41)] + ['label', 'difficulty']
df = pd.read_csv("E:\\ids_webapp\\backend\\model\\KDDTrain+.txt", names=column_names)

# Drop the 'difficulty' column
df.drop("difficulty", axis=1, inplace=True)

# Label encode categorical columns
categorical_cols = ['feature_1', 'feature_2', 'feature_3']  # protocol_type, service, flag
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le  # Save encoders in case you want to reuse later

# Binary encode label
df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

# Split features and label
X = df.drop("label", axis=1)
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# Save model AND feature names
joblib.dump((model, list(X.columns)), "backend/model/ids_model_with_features.joblib")
print("✅ Model + feature names saved as 'ids_model_with_features.joblib'")
