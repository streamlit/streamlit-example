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
from lipids_ranges import getLDLBPtarget
from diabetes import get_dm_advice
from anaemia import anaemia_analysis
from bmi import bmi_advice
#from dotenv import load_dotenv

#load_dotenv()
API_KEY = os.environ['API_KEY'] # API_KEY in streamlit secret

client = OpenAI(api_key=API_KEY)

ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

tab1, tab2 = st.tabs(["Main", "About"])

test_attributes = {}

measurements_list = """
    - Height
    - Weight
    - Cholesterol
    - Haemoglobin
    - Mean Corpuscular Volume (MCV)
    - Red Blood Cell (RBC)
    - Glucose
    - HbA1c
    - Blood Pressure (BP)
"""

with tab1:
    col1, mid, col2 = st.columns([1,1,10])
    with col1:
        st.image("https://i.ibb.co/869GgfZ/stethoscope-logo-text.jpg", width=100)
    with col2:
        st.subheader('Instructions:  \n1. Fill in the form below  \n 2. Upload a picture of your lab test results  \n3. Click "Generate my report!" button')

    # User inputs
    age = st.number_input("Enter your age", min_value=0, max_value=140, step=1,value="min")
    sex = st.selectbox("Select your sex", ["Female","Male"])
    race = st.selectbox("Select your race", ["Chinese", "Malay", "Indian", "Others"])
    smoker = st.checkbox("Are you a smoker?")
    stroke = st.checkbox("Have you ever had a stroke?")
    diabetes = st.checkbox("Do you have a history of diabetes?")
    heart_attack = st.checkbox("Have you ever had a heart attack?")
    ckd = st.checkbox("Do you have chronic kidney disease?")
    on_bp_meds = st.checkbox("Are you taking blood pressure medication?")
    systolic_bp = st.number_input("Enter your last recorded systolic blood pressure (leave blank if not available)", min_value=50,max_value=300,value=None)
            
    image = load_image()
        
    if st.button('Generate my report!'):
        # Save test attributes
        test_attributes["age"] = age
        test_attributes["sex"] = sex
        test_attributes["race"] = race
        test_attributes["smoker"] = smoker #true or false
        test_attributes["stroke"] = stroke
        test_attributes["diabetes"] = diabetes
        test_attributes["heart_attack"] = heart_attack
        test_attributes["ckd"] = ckd
        test_attributes["on_BP_meds"] = on_bp_meds
        test_attributes["systolic_blood_pressure"] = systolic_bp #null or integer
        # Extract text from image
        if not image: #Image not uploaded
            st.error("Upload an image of your test results first!",icon="🚨")
        else: # Image uploaded
            with st.status('Reading image...', expanded=True) as status:
                st.json(test_attributes)
                extracted_text,ocr_time = extract_text(image,ocr_model)
                st.markdown(extracted_text)
                st.success(f"Processed image in {ocr_time} seconds.")  # Use status instead of toast/success
                # Extract structured data from text using ChatGPT
                # TODO: PUT TRY AND ERROR IF FAIL 
                st.write("Extracting values from image...")
                response,test_results,extract_time = extract_values(client,extracted_text) # use chatgpt to extract
                st.json(test_results)
                st.text(response.usage)
                status.update(label="Analysed results!", state="complete", expanded=False)
                st.success(f"Extracted values in {extract_time} seconds.")  # Use status instead of toast/success
            # Insert YT logic
            print (test_results)
            print (test_attributes)
            #test_results test_attributes
            full_output = ""            
            dm = False
            anaemia = False 
            LDLBP = False 
            BMI = False 
            for key, value in test_results.items():
                print (f"looking at {key} and {value}")
                if value["test_found"]:
                    if key == "hb":
                        fbc_output = anaemia_analysis (test_results)
                        full_output += f"**Full Blood Count**  \n{fbc_output}  \n\n" # streamlit needs 2 whitespace before newline char
                    elif key == "ldl_cholesterol":
                        chol_output = getLDLBPtarget (test_attributes, test_results)
                        full_output += f"**Cholesterol and Blood Pressure**  \n{chol_output}  \n\n"
                    elif key == "glucose" or key == "hba1c":
                        if not dm:
                            glucose_output = get_dm_advice(test_attributes, test_results)
                            full_output += f"**Blood Sugar**  \n{glucose_output}  \n\n"
                            dm = True 
                    elif key == "systolic_bp":
                        if not test_results["hdl_cholesterol"]["test_found"]:
                            bp_output = "We need your cholesterol levels to interpret the blood pressure targets better. In general, aim for a blood pressure <140/90.  \n\n"
                            full_output += f"**Blood Pressure**  \n{bp_output}\n"
                    elif key == "weight" or key == "height":
                        if not BMI:
                            bmi_output = bmi_advice(test_results)
                            BMI = True 
                            full_output += f"**Height/Weight (BMI)**  \n{bmi_output}  \n\n"
            print(full_output)
            if full_output == "": # if no supported lab results found
                full_output = "No supported medical lab results detected in your image.  \nCheck if your image contains lab results listed in the About page."
                st.error(f"{full_output}",icon="🚨")
            else:
                st.subheader(':bookmark_tabs: Your Report')
                st.markdown(full_output)
            # print test results
            st.subheader(':test_tube: Measurement values detected')
            for test_name, test_info in test_results.items():
                if test_info["test_found"]:
                    st.markdown(f"**Test Name:** {test_name.replace('_', ' ').upper()}")
                    st.markdown(f"**Test Value:** {test_info['test_value']} {test_info['test_unit']}")
                    st.text("")
                            

with tab2:
    col1, mid, col2 = st.columns([1,1,10])
    with col1:
        st.image("https://i.ibb.co/869GgfZ/stethoscope-logo-text.jpg", width=100)
    with col2:
        st.text("")
        st.markdown("**Lab Lokun** is an AI-assisted app that interprets and explains blood and lab test reports to provide personalised health advice and recommendations using Singapore ACG guidelines. **Lab Lokun** is co-created by doctors and non-doctors who have interpreted indecipherable lab results to their friends and family too many times. :joy:")
    st.subheader('Lab measurements included for analysis')
    st.markdown(measurements_list)
    st.write('Other lab tests will be added soon...stay tuned!')    
    
st.caption('Disclaimer: Information provided through our app is for informational and educational purposes only and is not intended as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.')
