import pickle

# Load the model
model_path = 'model2.pkl'  
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Print out the type of the loaded object
print("Loaded model type:", type(model))

