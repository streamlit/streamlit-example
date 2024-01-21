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
    },
	"hb":{
		"test_found":True,
		"test_value":11,
		"test_unit":False,
		"test_ref_min":12,
		"test_ref_max":16
		},
}
#mcv need fl RBC need 10^6/uL
#returns tuple - bool whether anaemia, and bool whether iron deficient 
def anaemia_analysis (hbdict):
	print ("in anaemia analysis")
	hblevel = hbdict["hb"]["test_value"]
	emergency = True if hblevel < 7 else False 
	mcv = hbdict["mcv"]["test_value"]
	anaemia = bool(hblevel < hbdict["hb"]["test_ref_min"])
	antype = ""
	iron = False
	if anaemia:
		if mcv < hbdict["mcv"]["test_ref_min"]:
			mentzer = mcv/ hbdict["rbc_count"]["test_value"]
			if mentzer > 13:
				iron = True
			else :
				iron = False 
			antype = "microcytic"
		elif mcv > hbdict["mcv"]["test_ref_max"]:
			antype = "macrocytic"
		else: 
			antype = "normocytic"
		print(f"result of analysis {anaemia, antype, iron, emergency}\n")
	return (anaemia, antype, iron, emergency)

def get_anaemia_advice (input_tuple):
	print ("in anaemia advice")
	output_phrase = ""
	(anaemia_bool, anaemia_type, iron_deficient, emerg) = input_tuple
	if anaemia_bool:
		if emerg == True:
			output_phrase = "Your haemoglobin level is dangerously low. Please visit a doctor immediately."
		elif anaemia_type == "microcytic": 
			if iron_deficient == True:
				output_phrase = "you have anaemia, which could be due to iron deficiency. This can be caused by minor bleeding e.g. menstruation, or from the gastrointestinal tract. Visit your doctor for an assessment to rule out sources of bleeding. Consider taking iron supplements and foods rich in iron, such as green leafy vegetables, meat, especially red meat (beef, mutton, pork), seafood, and organs (kidney, liver)."
			else: 
				output_phrase = "you have anaemia, which could be related to genetic conditions such as thalassaemia. Visit your doctor for an assessment."
		elif anaemia_type == "macrocytic":
			output_phrase = "you have anaemia, which may be caused by low folate (vitamin B9) or vitamin B12 levels. Other causes may include chronic alcohol intake, thyroid problems, and liver problems. Consider taking more foods high in folate, such as broccoli, spinach, and brown rice, and foods high in vitamin B12, such as meat, milk, cheese and eggs."
		elif anaemia_type == "normocytic":
			output_phrase = "you have anaemia, which may be associated with chronic illness such as kidney disease, or chronic inflammatory conditions."
	return output_phrase 

#print (f"here is result: {get_anaemia_advice(anaemia_analysis (testdict))}")


