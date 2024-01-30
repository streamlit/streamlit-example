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
	output_phrase = "I didn't catch that"
	print ("in anaemia analysis")
	hblevel = hbdict["hb"]["test_value"]
	if hblevel < 7:
		return ":large_orange_circle: Your haemoglobin level is dangerously low. Please visit a doctor immediately."
	if hblevel < hbdict["hb"]["test_ref_min"]:
		if not hbdict["mcv"]["test_found"]:
			return ":large_orange_circle: You likely have anaemia, but there is not enough information to determine the cause. Visit a doctor if you have any concerns of blood loss."
		mcv = hbdict["mcv"]["test_value"]
		if mcv < hbdict["mcv"]["test_ref_min"]: #microcytic
			if not hbdict["rbc_count"]["test_found"]:
				return ":large_orange_circle: You likely have anaemia, but there is not enough information to determine the cause. Visit a doctor if you have any concerns of blood loss."
			mentzer = mcv/ hbdict["rbc_count"]["test_value"]
			if mentzer > 13:
				output_phrase = ":large_orange_circle: You likely have anaemia, which could be due to iron deficiency. This can be caused by minor bleeding e.g. menstruation, or from the gastrointestinal tract. Visit your doctor for an assessment to rule out sources of bleeding. Consider taking iron supplements and foods rich in iron, such as green leafy vegetables, meat, especially red meat (beef, mutton, pork), seafood, and organs (kidney, liver)."
			else :
				output_phrase = ":large_orange_circle: You likely have anaemia, which could be related to genetic conditions such as thalassaemia. Visit your doctor for an assessment." 
		elif mcv > hbdict["mcv"]["test_ref_max"]: # macrocytic
			output_phrase = ":large_orange_circle: You likely have anaemia, which may be caused by low folate (vitamin B9) or vitamin B12 levels. Other causes may include chronic alcohol intake, thyroid problems, and liver problems. Consider taking more foods high in folate, such as broccoli, spinach, and brown rice, and foods high in vitamin B12, such as meat, milk, cheese and eggs."
		else: #normocytic 
			output_phrase = ":large_orange_circle: You likely have anaemia, which may be associated with chronic illness such as kidney disease, or chronic inflammatory conditions."
	else:
		output_phrase = ":large_green_circle: You likely do not have anaemia."
	return output_phrase

#print (f"here is result: {anaemia_analysis (testdict)}")
