import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load the training and testing datasets
train_data = pd.read_csv("data/train.csv")
test_data = pd.read_csv("data/test.csv")

# Preprocessing
# Assuming the datasets have features X1, X2, ..., and a target column 'fake'
# Replace 'X1', 'X2', etc., with actual feature names from the datasets
X_train = train_data.drop(columns=['fake'])  # Replace 'fake' with the actual target column
y_train = train_data['fake']  # Replace 'fake' with the actual target column

X_test = test_data.drop(columns=['fake'])  # Replace 'fake' with the actual target column
y_test = test_data['fake']  # Replace 'fake' with the actual target column

# Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# Save the trained model
with open("random_forest_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model training completed and saved as 'random_forest_model.pkl'")