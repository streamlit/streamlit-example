import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import base64
import json
from openai import OpenAI
import cv2
from paddleocr import PaddleOCR

# REMOVE THIS BEFORE COPYING TO GITHUB!
API_KEY = os.environ['API_KEY']

test_attributes = {}

client = OpenAI(api_key=API_KEY)

template_prompt = """
Extract the items from the health screening result listed below into a json format, using the example json template. Ignore other items not listed in the json template. Output data types are "test_found" (True/False), "test_value" (float), "test_unit" (string in lower case), "test_ref_min" (float), "test_ref_max" (float). If test item is not found, output False for "test_found", and output False for the other values. If test is found but reference max, reference min, or reference range is not found, output False for "test_ref_min" and "test_ref_max". 

Example output json template
{
	"ldl_cholesterol": {
		"test_found":True,
		"test_value":20,
		"test_unit":"mmol/l",
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hdl_cholesterol": {
		"test_found":True,
		"test_value":20,
		"test_unit":"mmol/l",
		"test_ref_min":False,
		"test_ref_max":False
		},
	"total_cholesterol": {
		"test_found":True,
		"test_value":20,
		"test_unit":"mmol/l",
		"test_ref_min":False,
		"test_ref_max":False
		},
	"mcv":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hb:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"uric_acid:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hba1c:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"systolic_bp:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"diastolic_bp:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"height:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"weight:{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		}
}

Health screening result:
"""

def load_image():
    uploaded_file = st.file_uploader(label='Upload your test results image below:')
    if uploaded_file is not None:
        st.toast("Image uploaded")  # Toast message
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption='', use_column_width=True)  # Adjust width for mobile screens
        return image_data
        
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

ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
        
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
        result = ocr_model.ocr(image)
        extracted_text = ''
        for idx in range(len(result)):
            txt = result[idx][1][0]
            extracted_text += txt + " "
        ocr_end_time = time.time()
        ocr_time = int(ocr_end_time - ocr_start_time)
        st.markdown(extracted_text)
        st.success(f"Processed image in {ocr_time} seconds.")  # Use status instead of toast/success
        # Remove NRIC from extracted text
    
        # Extract structured data from text using ChatGPT
        # TODO: PUT TRY AND ERROR IF FAIL 
        extract_start_time = time.time()
        extract_prompt = f"{template_prompt} {extracted_text}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": extract_prompt}
            ]
        )
        test_results = json.loads(response.choices[0].message.content)
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
