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


template_prompt = """
Extract the items from the health screening result listed below into a json format, using the example json template. Ignore other items not listed in the json template. Output data types are "test_found" (True/False), "test_value" (float), "test_unit" (string), "test_ref_min" (float), "test_ref_max" (float). If test item is not found, output False for "test_found", and output False for the other values. If test is found but reference max, reference min, or reference range is not found, output False for "test_ref_min" and "test_ref_max". 
Convert height to metres and weight to kg.

Example output json template
{
	"ldl_cholesterol": {
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hdl_cholesterol": {
		"test_found":True,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"total_cholesterol": {
		"test_found":False,
		"test_value":False,
		"test_unit":False,
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
	"hb":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
    "rbc_count":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"glucose":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hba1c":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"systolic_bp":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"diastolic_bp":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"height":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"weight":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		}
}

Health screening result:
"""

def extract_values(client,extracted_text):
    extract_start_time = time.time()
    extract_prompt = f"{template_prompt} {extracted_text}"
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview", #gpt-3.5-turbo-1106
	seed=4022024,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": extract_prompt}
        ]
    )
    test_results = json.loads(response.choices[0].message.content)
    extract_end_time = time.time()
    extract_time = int(extract_end_time - extract_start_time)
    return response,test_results,extract_time
