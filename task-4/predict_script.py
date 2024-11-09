import requests
import pickle
import numpy as np
import tensorflow as tf

# Define the base URL for your FastAPI application.
# This URL is where the API is hosted and will be used to fetch data.
base_url = "https://database-design-yyzk.onrender.com"

# endpoint to fetch all loans.
endpoint = "/loans"


# Function to load a pre-trained TensorFlow model from a pickle file.
def load_model(model_path):
    """
    Load a TensorFlow model from a pickle file.
    
    Args:
        model_path (str): Path to the .pkl file containing the model's weights.

    Returns:
        tf.keras.Model: A TensorFlow Sequential model with the loaded weights, or None if an error occurs.
    """
    try:
        # Open the .pkl file in binary mode and load the saved weights.
        with open(model_path, 'rb') as f:
            weights = pickle.load(f)

        # Define the model architecture.
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.InputLayer(shape=(4,)))
        model.add(tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.L2(l2=1e-6)))
        model.add(tf.keras.layers.Dropout(0.1))
        model.add(tf.keras.layers.Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.L2(l2=1e-6)))
        model.add(tf.keras.layers.Dropout(0.1))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
        
        # Set the model weights from the loaded file.
        model.set_weights(weights)
        print("Model loaded successfully.")
        return model

    except Exception as e:
        print(f"Error loading model: {e}")
        return None


# Function to fetch all loan records from the API.
def fetch_all_loans():
    """
    Fetch all loan data from the FastAPI endpoint.

    Returns:
        list: A list of loan records in JSON format, or None if an error occurs.
    """
    try:
        response = requests.get(base_url + endpoint)
        # Check if the HTTP response status code is 200 (OK).
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


# Function to get the latest loan entry based on the highest 'id'.
def get_latest_loan(loans):
    """
    Retrieve the latest loan entry by sorting the list based on 'id'.

    Args:
        loans (list): A list of loan records.

    Returns:
        dict: The latest loan record, or None if no loans are found.
    """
    if loans:
        latest_loan = max(loans, key=lambda x: x['id'])
        print("Latest Loan Data:", latest_loan)
        return latest_loan
    else:
        print("No loans found.")
        return None


# Function to prepare the input data for the model prediction.
def prepare_input_data(loan_data):
    """
    Prepare the input data for making a prediction.

    Args:
        loan_data (dict): A dictionary containing loan details.

    Returns:
        np.array: A NumPy array formatted for the model input.
    """
    input_data = np.array([[  # To convert the data into a 2D NumPy array.
        loan_data['person_home_ownership_type_id'],
        loan_data['loan_int_rate'],
        loan_data['loan_percent_income'],
        1 if loan_data['cb_person_default_on_file'] == 'Y' else 0  # To convert 'Y'/'N' to binary (1/0).
    ]])
    
    print(f"Prepared input data: {input_data}")
    return input_data


# Function to interpret the model's prediction.
def interpret_prediction(prediction):
    """
    Interpret the model's prediction based on a threshold of 0.5.

    Args:
        prediction (float): The predicted value (between 0 and 1).
    """
    if prediction >= 0.5:
        print("Prediction: Positive class (e.g., loan approval or default)")
    else:
        print("Prediction: Negative class (e.g., loan rejection or no default)")


# Function to make a prediction using the loaded model.
def make_prediction(model, input_data):
    """
    Use the loaded model to make a prediction.

    Args:
        model (tf.keras.Model): The pre-trained TensorFlow model.
        input_data (np.array): The input data for prediction.

    Returns:
        float: The prediction result, or None if an error occurs.
    """
    if model and input_data is not None:
        try:
            prediction = model.predict(input_data)
            print("Prediction:", prediction)
            prediction_result = prediction[0][0]  
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
    # Load the saved model from the specified file path.
    model_path = 'model2.pkl'
    model = load_model(model_path)

    # Fetch all loans from the FastAPI endpoint.
    loans = fetch_all_loans()

    # If loans were successfully fetched, get the latest loan entry.
    if loans:
        latest_loan = get_latest_loan(loans)
        if latest_loan:
            # Prepare the input data for prediction using the latest loan.
            input_data = prepare_input_data(latest_loan)
            
            # Make a prediction using the pre-trained model.
            prediction = make_prediction(model, input_data)
            print(f"Prediction result: {prediction}")
        else:
            print("Could not retrieve the latest loan.")
    else:
        print("Could not retrieve loans.")
