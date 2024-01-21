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


def load_image(ocr_model):
    uploaded_file = st.file_uploader(label='Upload your test results image below:')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption='', use_column_width=True)  # Adjust width for mobile screens
        return image_data
        

def extract_text(image):
    result = ocr_model.ocr(image)
    result = result[0] #idk why this needs a result[0] instead of result for Github
    extracted_text = ''
    for idx in range(len(result)):
        txt = result[idx][1][0]
        extracted_text += txt + " "
    return extracted_text
