import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import base64
import json
import cv2
import re
from openai import OpenAI
from paddleocr import PaddleOCR

def load_image():
    uploaded_file = st.file_uploader(label='Upload your test results image below:')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption='', use_column_width=True)  # Adjust width for mobile screens
        return image_data

def remove_nric(text):
    pattern = r'[STFG]\d{7}[A-Z]'
    replaced_text = re.sub(pattern, ' ', text)
    return replaced_text

def extract_text(image,ocr_model):
    ocr_start_time = time.time()
    result = ocr_model.ocr(image)
    result = result [0] #idk why this needs a result[0] instead of result for Github
    extracted_text = ''
    for idx in range(len(result)):
        txt = result[idx][1][0]
        extracted_text += str(txt) + " "
    extracted_text_clean = remove_nric(extracted_text)
    ocr_end_time = time.time()
    ocr_time = int(ocr_end_time - ocr_start_time)
    return extracted_text_clean, ocr_time
