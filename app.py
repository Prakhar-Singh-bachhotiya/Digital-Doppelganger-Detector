from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

# Load the trained model
with open("random_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Create an `index.html` for user input

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON input
        data = request.get_json()
        if not data or 'username' not in data:
            return jsonify({'error': 'Invalid input. Please provide a username.'}), 400

        username = data.get('username', 'testuser')  # Default value if empty

        # Define all features used during training
        features = {
            'profile pic': 1,  # Mock value (could be a boolean or integer)
            'nums/length username': sum(char.isdigit() for char in username) / len(username) if username else 0,
            'fullname words': 2,  # Mock value
            'nums/length fullname': 0,  # Mock value
            'name==username': 0,  # Mock value (check if name is equal to username)
            'description length': 80,  # Mock value (could be length of description text)
            'external URL': 1,  # Mock value (1 if there's an external URL)
            'private': 0,  # Mock value (0 for public account)
            '#posts':5,  # Mock value (number of posts)
            '#followers': 0,  # Mock value (number of followers)
            '#follows': 900  # Mock value (number of follows)
        }

        # Convert the features to a DataFrame
        df = pd.DataFrame([features])

        # List all feature columns that the model was trained with
        trained_features = [
            'profile pic', 'nums/length username', 'fullname words', 'nums/length fullname',
            'name==username', 'description length', 'external URL', 'private',
            '#posts', '#followers', '#follows'
        ]

        # Ensure the order of columns matches the training data
        df = df[trained_features]

        # Make prediction
        prediction = model.predict(df)[0]  # Model prediction

        # Map prediction result to "Real" or "Fake"
        result = "Real" if prediction == 0 else "Fake"

        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)