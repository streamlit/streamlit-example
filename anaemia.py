testdict = {
    "mcv":{
		"test_found":True,
		"test_value":60,
		"test_unit":False,
		"test_ref_min":85,
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
		"test_found":True,
		"test_value":11,
		"test_unit":False,
		"test_ref_min":12,
		"test_ref_max":16
		},
}
#mcv need fl RBC need 10^6/uL
def anaemia_analysis (hbdict):
    hblevel = hbdict["hb"]["test_value"]
    anaemia = bool(hblevel < hbdict["hb"]["test_ref_min"])
    
    return result