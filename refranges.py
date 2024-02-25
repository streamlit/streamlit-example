import json 
from lipids_ranges import getLDLtarget
from diabetes import get_dm_advice
from anaemia import anaemia_analysis, get_anaemia_advice

testdict = {
	"ldl_cholesterol": {
		"test_found":True,
		"test_value":2.0,
		"test_unit":"mmol/l",
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hdl_cholesterol": {
		"test_found":True,
		"test_value":1.2,
		"test_unit":"mmol/l",
		"test_ref_min":False,
		"test_ref_max":False
		},
	"total_cholesterol": {
		"test_found":True,
		"test_value":5.0,
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


