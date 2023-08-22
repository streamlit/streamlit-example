import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

# Set display options to show all columns and rows without truncation
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows



class ColumnDropper(BaseEstimator,TransformerMixin):
        def __init__(self):
            pass

        def fit(self, X, Y = None):
            return self

        def transform(self, X, Y = None):
            X = X.drop(['isFlaggedFraud'], axis = 1)
            return X
def newDesAmountAfterTransactionColumn(inputDf):
            destAmountChange = inputDf['newbalanceDest'] - inputDf['oldbalanceDest']
            inputDf['DestAmountAfterTransaction'] = abs(destAmountChange)
            return inputDf
def applyCondition(inputDf):
            inputDf = inputDf[(inputDf['amount'] != 0) & (inputDf['DestAmountAfterTransaction'] != 0)]
            return inputDf

def transformOneHot(inputDf, selected_payment_type):
            type_selected = selected_payment_type
            # dummies = pd.get_dummies(inputDf['type'])
            type_list = {"CASH_IN":'', "CASH_OUT":'', "DEBIT":'', "PAYMENT":'', "TRANSFER":''}
            my_dict = type_list.fromkeys(type_list, 0)
            # print(my_dict)
            if type_selected in my_dict.keys():
                my_dict.update({type_selected: 1})
            my_dict = {k:[v] for k,v in my_dict.items()} 
            my_dict = pd.DataFrame.from_dict(my_dict)
            # print(my_dict)
            inputDf  = pd.concat([inputDf , my_dict], axis = 1)
            inputDf = inputDf.drop(['type', 'nameOrig', 'nameDest', 'isFraud', "PAYMENT"], axis = 1)
            # print(inputDf.head())
            return inputDf       

def preprocessing(inputDf, selected_payment_type):
            df_1 = newDesAmountAfterTransactionColumn(inputDf)
            df_2 = applyCondition(df_1)
            df_2 = transformOneHot(df_2, selected_payment_type)
            
            # main_pipeline = Pipeline([
            # ('dropColumns',ColumnDropper() ),
            # ("MinMaxScaler", MinMaxScaler()),
            # ('RandomClassifier',RandomForestClassifier(n_estimators = 500, max_depth=7, random_state=42) )
    
            # ])
            print(df_2)
            return df_2
    

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
            "step": [steps],
            "type": [selected_payment_type],
            "amount": [amount],
            "nameOrig": ["Dummy Value"],
            "oldbalanceOrg": [oldbalanceOrg],
            "newbalanceOrig": [newbalanceOrig],
            "nameDest": ["Dummy Value"],
            "oldbalanceDest": [oldbalanceDest],
            "newbalanceDest": [newbalanceDest],
            "isFraud": [0],
            "isFlaggedFraud": [0],
        })
        # print('before',input)
        # input_data_df = pd.DataFrame(input_data)
        processed_input_df = preprocessing(input_data, selected_payment_type)
        print('processed data',processed_input_df)
        print(input_data)
        loaded_model = joblib.load('model_ahshik.pkl')
        # # Make a prediction using the loaded model
        prediction = loaded_model.predict(processed_input_df)
        # print('after',input_data)
        # print(prediction)
        
        # Display the prediction result
        if prediction[0] == 1:
            st.error("Fraud detected!")
        else:
            st.success("No fraud detected.")

if __name__ == "__main__":
    main()
