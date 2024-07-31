import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the models
with open('models/Machine_failure.pkl', 'rb') as file:
    failure_model = pickle.load(file)

with open('models/type_of_failure.pkl', 'rb') as file:
    type_of_failure_model = pickle.load(file)

# Function to encode the 'Type' feature
def encode_type(type_value):
    encoding = {'Low': 0, 'Medium': 1, 'High': 2}
    return encoding[type_value]

# Normalize the input features
def normalize_features(features):
    scaler = MinMaxScaler()
    return scaler.fit_transform(np.array(features).reshape(1, -1))

# Function to decode the type of failure
def decode_type_of_failure(type_code):
    decoding = {
        0: 'Heat dissipation failure',
        1: 'No failure',
        2: 'Over strain failure',
        3: 'Power failure',
        4: 'Random failure',
        5: 'Tool wear failure'
    }
    return decoding[type_code]

# Page configuration
st.set_page_config(
    page_title="Machine Failure Prediction",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="auto"
)

# Title and description
st.title("🔧 Machine Failure and Type of Failure Prediction")
st.write("### Predict whether a machine will fail and the type of failure based on the input features.")
st.markdown("---")

# Input features
st.sidebar.header("Input Features")
type_value = st.sidebar.selectbox("Type", ["Low", "Medium", "High"])
rotational_speed = st.sidebar.number_input("Rotational speed [rpm]", min_value=0)
torque = st.sidebar.number_input("Torque [Nm]", min_value=0.0)
tool_wear = st.sidebar.number_input("Tool wear [min]", min_value=0)
air_temp = st.sidebar.number_input("Air temperature [C]", min_value=0.0)
process_temp = st.sidebar.number_input("Process temperature [C]", min_value=0.0)

# Encode and normalize the input features
encoded_type = encode_type(type_value)
features = [encoded_type, rotational_speed, torque, tool_wear, air_temp, process_temp]
normalized_features = normalize_features(features)

# Predict button
if st.button("Predict"):
    with st.spinner('Making predictions...'):
        failure_prediction = failure_model.predict(normalized_features)
        type_of_failure_prediction = type_of_failure_model.predict(normalized_features)

    # Display predictions
    st.markdown("### Prediction Results")
    if failure_prediction[0] == 0:
        st.success("Prediction: No Failure")
    else:
        st.error("Prediction: Failure")

    st.info(f"Type of Failure Prediction: {decode_type_of_failure(type_of_failure_prediction[0])}")

# Footer
st.markdown("---")
st.write("Developed by Alok Shukla")

# Add some CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stSpinner {
        margin: 0 auto;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
