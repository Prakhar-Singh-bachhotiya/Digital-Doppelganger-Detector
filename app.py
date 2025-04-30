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

@app.route('/add_features')
def add_features():
    return render_template('add_features.html')  # Create an `add_features.html` file

@app.route('/predict_features', methods=['POST'])
def predict_features():
    try:
        # Parse JSON input
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input. Please provide feature data.'}), 400

        # Extract features from input
        features = {
            'profile pic': data.get('profile pic', 1),
            'nums/length username': data.get('nums/length username', 0),
            'fullname words': data.get('fullname words', 0),
            'nums/length fullname': data.get('nums/length fullname', 0),
            'name==username': data.get('name==username', 0),
            'description length': data.get('description length', 80),
            'external URL': data.get('external URL', 1),
            'private': data.get('private', 0),
            '#posts': data.get('#posts', 0),
            '#followers': data.get('#followers', 0),
            '#follows': data.get('#follows', 0)
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
    
# ********************************************
# send querry part fine till above    

from flask import Flask, request, jsonify
import smtplib

@app.route('/send_query', methods=['POST'])
def send_query():
    try:
        data = request.get_json()
        customer_name = data.get('customerName')
        customer_email = data.get('customerEmail')
        query = data.get('query')

        if not customer_name or not customer_email or not query:
            return jsonify({'error': 'All fields are required.'}), 400

        # Email credentials (replace with your email credentials)
        sender_email = "psbcheeku@gmail.com"
        sender_password = "emyh mkrl eqtg jhpa"
        support_email = "psbcheeku@gmail.com"

        # Send email to support team
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email,
                support_email,
                f"Subject: New Query from {customer_name}\n\n"
                f"Name: {customer_name}\n"
                f"Email: {customer_email}\n"
                f"Query: {query}"
            )

        # Send confirmation email to customer
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email,
                customer_email,
                f"Subject: Query Received\n\n"
                f"Dear {customer_name},\n\n"
                f"Thank you for reaching out to us. Your query has been recorded and will be responded to within 2-3 business days.\n\n"
                f"Best regards,\n"
                f"InstaVerify Support Team"
            )

        return jsonify({'message': 'Query sent successfully.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)