import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Set display options to show all columns and rows without truncation
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows

loaded_model = joblib.load('model.pkl')

def data_preprocessing(data):
    features = data.drop(columns=['isFraud'])
    # List of columns to drop
    columns_to_drop = ['nameOrig', 'nameDest', 'isFlaggedFraud']

    # List of categorical columns to one-hot encode
    categorical_columns = ['amount_cluster', 'type']

    # List of numerical columns to normalize
    numerical_columns = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest','transaction_change', 'dest_balance_change', 'day_of_week','hour_of_day']

    # Custom transformer for feature engineering
    class FeatureEngineeringTransformer(BaseEstimator, TransformerMixin):
        def __init__(self):
            pass

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            data = X.copy()

            # Calculate Transaction Change
            data['transaction_change'] = data['newbalanceOrig'] - data['oldbalanceOrg']

            # Calculate Destination Balance Change
            data['dest_balance_change'] = data['newbalanceDest'] - data['oldbalanceDest']

            # Extract Day of the Week and Hour of the Day
            data['day_of_week'] = data['step'] % 7
            data['hour_of_day'] = data['step'] % 24

            # Create Transaction Amount Clusters
            amount_bins = [0, 100, 500, 1000, np.inf]
            amount_labels = ['small', 'medium', 'large', 'extra_large']
            data['amount_cluster'] = pd.cut(data['amount'], bins=amount_bins, labels=amount_labels)
            return data

    # Create a ColumnTransformer for one-hot encoding and normalization
    preprocessor = ColumnTransformer(
        transformers=[
            ('drop', 'drop', columns_to_drop),
            ('cat', OneHotEncoder(), categorical_columns),
            ('num', StandardScaler(), numerical_columns)
        ],
        remainder='passthrough'  # Keep non-categorical, non-numerical columns unchanged
    )

    # Create the data preprocessing pipeline
    data_pipeline = Pipeline(steps=[
        ('feature_engineering', FeatureEngineeringTransformer()),
        ('preprocessor', preprocessor)
    ])

    # Apply the pipeline to your data
    data_preprocessed = data_pipeline.fit_transform(features)
    return data_preprocessed

def main():
    st.title("Fraud Detection App")

    # Create input fields for user to input features
    steps = st.slider("Step", min_value=1, max_value=744, value=350)
    payment_type_options = ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    selected_payment_type = st.selectbox("Select a category", payment_type_options)
    amount = st.number_input("Amount", min_value=0.0, value=0.0)
    oldbalanceOrg = st.number_input("Current Balance At Origin", min_value=0.0, value=0.0)
    newbalanceOrig = st.number_input("New Balance At Origin", min_value=0.0, value=0.0)
    oldbalanceDest = st.number_input("Current Balance At Destination", min_value=0.0, value=0.0)
    newbalanceDest = st.number_input("New Balance At Destination", min_value=0.0, value=0.0)
    
    # Create a button to predict
    if st.button("Predict"):
        
        #Prepare the input data as a DataFrame.
        #Note: Only the value in the index 0 of the data array is actual input. The rest are added to make sure the one hot encoder is working the same as the training pipeline. 
        input_data = pd.DataFrame({
            "step": [steps, steps, steps,steps,steps,steps,steps],
            "type": [selected_payment_type, "CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER", "TRANSFER"],
            "amount": [amount, 1, 101, 501, 1001, 10001, 0],
            "nameOrig": ["Dummy Value", "Dummy Value","Dummy Value","Dummy Value","Dummy Value","Dummy Value","Dummy Value"],
            "oldbalanceOrg": [oldbalanceOrg, 0, 0, 0, 0, 0, 0],
            "newbalanceOrig": [newbalanceOrig, 0, 0, 0, 0, 0, 0],
            "nameDest": ["Dummy Value","Dummy Value","Dummy Value","Dummy Value","Dummy Value","Dummy Value","Dummy Value"],
            "oldbalanceDest": [oldbalanceDest, 0, 0, 0, 0, 0,0],
            "newbalanceDest": [newbalanceDest, 0, 0, 0, 0, 0,0],
            "isFraud": [0, 0, 0, 0, 0, 0,0],
            "isFlaggedFraud": [0, 0, 0, 0, 0, 0,0]
        })
        
        input_data = pd.DataFrame(data_preprocessing(input_data))

        # Make a prediction using the loaded model
        prediction = loaded_model.predict(input_data)
        
        print(prediction)
        
        # Display the prediction result
        if prediction[0] == 1:
            st.error("Fraud detected!")
        else:
            st.success("No fraud detected.")

if __name__ == "__main__":
    main()
