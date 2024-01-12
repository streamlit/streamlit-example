import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import base64
from openai import OpenAI
import cv2
from paddleocr import PaddleOCR

st.title('Explain my test results please!')
st.header('Instructions')
st.markdown('Take a picture of your lab test results, upload it, and we will explain it to you!')

def load_image():
    uploaded_file = st.file_uploader(label='Upload your test results image below:')
    if uploaded_file is not None:
        st.toast("Image uploaded")  # Toast message
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption='', use_column_width=True)  # Adjust width for mobile screens
        return image_data

ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
        
image = load_image()
    
if st.button('Process Image'):
    start_time = time.time()
    result = ocr_model.ocr(image)
    inner_result = result[0]
    extracted_text = ''
    for idx in range(len(result)):
        txt = result[idx][1][0]
        extracted_text += txt + " "
    end_time = time.time()
    extract_time = int(end_time - start_time)
    st.markdown(extracted_text)
    st.success(f"Extracted values in {extract_time} seconds.")  # Use status instead of toast/success
    
st.caption('Disclaimer: Not medical advice, not liable, blah')
