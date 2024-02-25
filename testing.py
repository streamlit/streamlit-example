
from lipids_ranges import getLDLBPtarget
from diabetes import get_dm_advice
from anaemia import anaemia_analysis
from bmi import bmi_advice

test_attributes = {
    "age":57,
    "sex":"male",
    "race":"Chinese",
    "smoker":False,
    "stroke":False,
    "diabetes":False,
    "heart_attack":False,
    "ckd":False,
    "on_BP_meds":False,
    "systolic_blood_pressure": 120
}

test_results = {
    'ldl_cholesterol': {'test_found': False, 'test_value': 2.2, 'test_unit': 'mmol/l', 'test_ref_min': False, 'test_ref_max': False}, 
    'hdl_cholesterol': {'test_found': False, 'test_value': 1, 'test_unit': 'mmol/l', 'test_ref_min': False, 'test_ref_max': False}, 
    'total_cholesterol': {'test_found': False, 'test_value': 3.7, 'test_unit': 'mmol/l', 'test_ref_min': False, 'test_ref_max': False}, 
    'mcv': {'test_found': True, 'test_value': 100, 'test_unit': False, 'test_ref_min': 85, 'test_ref_max': 90}, 
    'hb': {'test_found': True, 'test_value': 10, 'test_unit': 'g/dL', 'test_ref_min': 11.5, 'test_ref_max': 15.5},
    'rbc_count': {'test_found': True, 'test_value': 4.2, 'test_unit': False, 'test_ref_min': False, 'test_ref_max': False}, 
    'glucose': {'test_found': False, 'test_value': False, 'test_unit': 'mmol/L', 'test_ref_min': False, 'test_ref_max': False}, 
    'hba1c': {'test_found': False, 'test_value': 6.0, 'test_unit': '%', 'test_ref_min': False, 'test_ref_max': False}, 
    'systolic_bp': {'test_found': False, 'test_value': False, 'test_unit': 'mmHg', 'test_ref_min': False, 'test_ref_max': False}, 
    'diastolic_bp': {'test_found': False, 'test_value': False, 'test_unit': 'mmHg', 'test_ref_min': False, 'test_ref_max': False}, 
    'height': {'test_found': False, 'test_value': 1.61, 'test_unit': 'm', 'test_ref_min': False, 'test_ref_max': False}, 
    'weight': {'test_found': False, 'test_value': 58, 'test_unit': 'kg', 'test_ref_min': False, 'test_ref_max': False}
}

for key, value in test_results.items():
    print (f"looking at {key} and {value}")
    if value["test_found"]:
        if key == "hb":
            print (f"FBC {anaemia_analysis (test_results)}")
        elif key == "ldl_cholesterol":
            print (f"LDL/BP {getLDLBPtarget (test_attributes, test_results)}")
        elif key == "glucose":
            print (f"glucose {get_dm_advice(test_attributes, test_results)}")
        elif key == "systolic_bp":
            if not test_results["total_cholesterol"]["test_found"] or not test_results["hdl_cholesterol"]["test_found"]:
                print("we need your cholesterol levels to interpret the blood pressure targets better. In general, aim for a blood pressure <140/90.")
        elif key == "weight":
            print (f"BMI {bmi_advice(test_results)}")