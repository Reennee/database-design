import requests
import pickle
import numpy as np
import tensorflow as tf

# Define base URL for FastAPI app
base_url = "https://database-design-yyzk.onrender.com"

# Define endpoint to fetch all loans
endpoint = "/loans"

# Load model from .pkl file
def load_model(model_path):
    try:
        with open(model_path, 'rb') as f:
            weights = pickle.load(f)
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.InputLayer(shape=(4,)))
            model.add(tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.L2(l2=1e-6)))
            model.add(tf.keras.layers.Dropout(0.1))
            model.add(tf.keras.layers.Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.L2(l2=1e-6)))
            model.add(tf.keras.layers.Dropout(0.1))
            model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
            model.set_weights(weights)
            print("Model loaded successfully.")
            return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Fetch all loans from API
def fetch_all_loans():
    try:
        response = requests.get(base_url + endpoint)
        # Check if response was successful (status code 200)
        if response.status_code == 200:
            loans = response.json()
            print(f"Successfully retrieved {len(loans)} loans.")
            return loans
        else:
            print(f"Failed to fetch loans. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Prepare input data for prediction
def prepare_input_data(person_home_ownership_type_id, loan_int_rate, loan_percent_income, cb_person_default_on_file):
    # Convert inputs to the expected format for the model
    input_data = np.array([[
        person_home_ownership_type_id,  
        loan_int_rate,
        loan_percent_income,
        1 if cb_person_default_on_file == 'Y' else 0  
    ]])
    
    print(f"Prepared input data: {input_data}")
    return input_data

# Interpret prediction based on a threshold
def interpret_prediction(prediction):
    if prediction >= 0.5:
        print("Prediction: loan approval")
    else:
        print("Prediction: loan rejection")

# Make prediction using loaded model
def make_prediction(model, input_data):
    if model and input_data is not None:
        try:
            prediction = model.predict(input_data)
            print("Prediction:", prediction)
            prediction_result = prediction[0][0]  # Extract the result from the prediction array
            interpret_prediction(prediction_result)  
            return prediction_result
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    else:
        print("Model or input data is missing.")
        return None

# Main script execution
if __name__ == "__main__":
    # Load saved model
    model_path = 'model2.pkl'
    model = load_model(model_path)

    # Accept user input for prediction
    print("Please enter the following details for loan prediction:")

    # Getting user input
    person_home_ownership_type_id = int(input("Enter Home Ownership Type ID: "))
    loan_int_rate = float(input("Enter Loan Interest Rate: "))
    loan_percent_income = float(input("Enter Loan Percent Income: "))
    cb_person_default_on_file = input("Enter CB Person Default on File (Y for Yes, N for No): ").upper()

    # Prepare input data for prediction
    input_data = prepare_input_data(person_home_ownership_type_id, loan_int_rate, loan_percent_income, cb_person_default_on_file)
    
    # Make prediction using model
    prediction = make_prediction(model, input_data)
    print(f"Prediction result: {prediction}")
