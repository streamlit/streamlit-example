import json 
from lipids_ranges import getLDLtarget

testdict = {
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
    "rbc_count":{
 		"test_found":True,
		"test_value":60,
		"test_unit":False,
		"test_ref_min":85,
		"test_ref_max":False       
    }
	"hb":{
		"test_found":False,
		"test_value":False,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"uric_acid":{
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

test_attributes = {
    "age" : 35, 
    "sex" :"male", #0 for male, 1 for female 
    "smoker" : True, 
    "stroke" : False,
    "diabetes" : False ,
    "heart_attack" : False ,
    "race" :"chinese",
    "systolic_blood_pressure" : 140,
    "on_BP_meds" : False,
    "total_cholesterol" : testdict["CHOLESTEROL"], #masterdict["CHOLESTEROL"]
    "hdl_cholesterol" : testdict["HDL CHOLESTEROL"] #masterdict["HDL CHOLESTEROL"]
}