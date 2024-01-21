import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import base64
import json
import cv2
from openai import OpenAI
from paddleocr import PaddleOCR
from image_loading import load_image, extract_text
from chatgpt_values import extract_values

# REMOVE THIS BEFORE COPYING TO GITHUB!
API_KEY = os.environ['OPENAI_KEY']
client = OpenAI(api_key=API_KEY) #etest

ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

test_attributes = {}

st.title('Explain my test results please!')
st.header('Instructions')
st.markdown('Answer the questions, take a picture of your lab test results, upload it, and we will explain it to you!')
    
# User inputs
age = st.number_input("Enter your age", min_value=0, max_value=140, step=1,value="min")
sex = st.selectbox("Select your sex", ["Female","Male"])
race = st.selectbox("Select your race", ["Chinese", "Malay", "Indian", "Others"])
smoker = st.checkbox("Are you a smoker?")
stroke = st.checkbox("Have you ever had a stroke?")
diabetes = st.checkbox("Do you have a history of diabetes?")
heart_attack = st.checkbox("Have you ever had a heart attack?")
on_bp_meds = st.checkbox("Are you taking blood pressure medication?")
systolic_bp = st.number_input("Enter your last recorded systolic blood pressure (leave blank if not available)", min_value=50,max_value=300,value=None)
        
image = load_image()
    
if st.button('Analyse my results'):
    # Save test attributes
    test_attributes["age"] = age
    test_attributes["sex"] = sex
    test_attributes["race"] = race
    test_attributes["smoker"] = smoker #true or false
    test_attributes["stroke"] = stroke
    test_attributes["diabetes"] = diabetes
    test_attributes["heart_attack"] = heart_attack
    test_attributes["on_BP_meds"] = on_bp_meds
    test_attributes["systolic_blood_pressure"] = systolic_bp #null or integer
    st.json(test_attributes)
    # Extract text from image
    if not image: #Image not uploaded
        st.error("Upload an image of your test results first!",icon="🚨")
    else: # Image uploaded
        ocr_start_time = time.time()
        extracted_text = extract_text(image,ocr_model)
        ocr_end_time = time.time()
        ocr_time = int(ocr_end_time - ocr_start_time)
        st.markdown(extracted_text)
        st.success(f"Processed image in {ocr_time} seconds.")  # Use status instead of toast/success
        # Remove NRIC from extracted text
    
        # Extract structured data from text using ChatGPT
        # TODO: PUT TRY AND ERROR IF FAIL 
        extract_start_time = time.time()
        response,test_results = extract_values(client,extracted_text) # use chatgpt to extract
        st.json(test_results)
        st.text(response.usage)
        extract_end_time = time.time()
        extract_time = int(extract_end_time - extract_start_time)
        st.success(f"Extracted values in {extract_time} seconds.")  # Use status instead of toast/success
        for test_name, test_info in test_results.items():
            if test_info["test_found"]:
                st.markdown(f"**Test Name:** {test_name.replace('_', ' ').upper()}")
                st.markdown(f"**Test Value:** {test_info['test_value']} {test_info['test_unit']}")
                #st.markdown(f"**Reference Range:** {test_info['test_ref_min']} - {test_info['test_ref_max']} {test_info['test_unit']}")
                st.text("")
        # Insert YT logic
        
st.caption('Disclaimer: Not medical advice, not liable, blah')
