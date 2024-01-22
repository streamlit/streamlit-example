from lipids_ranges import getLDLBPtarget
from diabetes import get_dm_advice
from anaemia import anaemia_analysis, get_anaemia_advice
from bmi import bmi_advice

test_attributes = {
    "age":57
    "sex":"Female"
    "race":"Chinese"
    "smoker":false
    "stroke":false
    "diabetes":false
    "heart_attack":false
    "ckd":false
    "on_BP_meds":false
    "systolic_blood_pressure":NULL
}

test_results = {
    'ldl_cholesterol': {'test_found': True, 'test_value': 2.2, 'test_unit': 'mmol/l', 'test_ref_min': False, 'test_ref_max': False}, 
    'hdl_cholesterol': {'test_found': True, 'test_value': 1, 'test_unit': 'mmol/l', 'test_ref_min': False, 'test_ref_max': False}, 
    'total_cholesterol': {'test_found': True, 'test_value': 3.7, 'test_unit': 'mmol/l', 'test_ref_min': False, 'test_ref_max': False}, 
    'mcv': {'test_found': False, 'test_value': False, 'test_unit': False, 'test_ref_min': False, 'test_ref_max': False}, 
    'hb': {'test_found': True, 'test_value': 15.6, 'test_unit': 'g/dL', 'test_ref_min': False, 'test_ref_max': False}, 
    'rbc_count': {'test_found': False, 'test_value': False, 'test_unit': False, 'test_ref_min': False, 'test_ref_max': False}, 
    'glucose': {'test_found': True, 'test_value': 5.3, 'test_unit': 'mmol/L', 'test_ref_min': False, 'test_ref_max': False}, 
    'hba1c': {'test_found': True, 'test_value': 5.8, 'test_unit': '%', 'test_ref_min': False, 'test_ref_max': False}, 
    'systolic_bp': {'test_found': True, 'test_value': 141, 'test_unit': 'mmHg', 'test_ref_min': False, 'test_ref_max': False}, 
    'diastolic_bp': {'test_found': True, 'test_value': 73, 'test_unit': 'mmHg', 'test_ref_min': False, 'test_ref_max': False}, 
    'height': {'test_found': True, 'test_value': 1.61, 'test_unit': 'm', 'test_ref_min': False, 'test_ref_max': False}, 
    'weight': {'test_found': True, 'test_value': 58, 'test_unit': 'kg', 'test_ref_min': False, 'test_ref_max': False}
}

for key, value in test_results.items():
    print (f"looking at {key} and {value}")
    if value["test_found"]:
        if key == "mcv":
            print (f"FBC {get_anaemia_advice(anaemia_analysis (test_results))}")
            st.write (f"FBC {get_anaemia_advice(anaemia_analysis (test_results))}")
        elif key == "ldl_cholesterol":
            st.write (f"LDL/BP {getLDLBPtarget (test_attributes, test_results)}")
            print (f"LDL/BP {getLDLBPtarget (test_attributes, test_results)}")
        elif key == "glucose":
            st.write (f"glucose {get_dm_advice(test_attributes, test_results)}")
            print (f"glucose {get_dm_advice(test_attributes, test_results)}")
        elif key == "systolic_bp":
            if not test_results["ldl_cholesterol"]["test_found"]:
                st.write("we need your cholesterol levels to interpret the blood pressure targets better. In general, aim for a blood pressure <140/90.")
        elif key == "weight":
            st.write (f"BMI {bmi_advice(test_results)}")