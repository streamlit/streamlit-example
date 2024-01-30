testdict = {
    "glucose":{
		"test_found":True,
		"test_value":6.5,
		"test_unit":"mmol/l",
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hba1c":{
		"test_found":True,
		"test_value":6.4,
		"test_unit":"%",
		"test_ref_min":False,
		"test_ref_max":False
		}
}

test_attributes = {
    "age" : 40, 
    "sex" :"male", #0 for male, 1 for female 
    "smoker" : True, 
    "stroke" : False,
    "diabetes" : True,
    "ckd" : False,
    "heart_attack" : False ,
    "race" :"indian",
    "systolic_blood_pressure" : 120,
    "on_BP_meds" : False
}


def get_dm_advice(inputattributes, inputdict):
    print ("in dm advice")
    output_phrase = "I didn't catch that."
    lifestyle = False
    #known dm
    a1c_value = inputdict["hba1c"]["test_value"] if inputdict["hba1c"]["test_found"] else 0 
    glucose_value = inputdict["glucose"]["test_value"] if inputdict["glucose"]["test_found"] else 0 
    if inputattributes["diabetes"]:
        if a1c_value >0:
            if inputattributes["age"] >= 80:
                a1ctarget = 8
            elif inputattributes["age"] <=40:
                a1ctarget = 6.5 
            else:
                a1ctarget = 7.0 
            if a1c_value > a1ctarget:
                output_phrase = ":large_orange_circle:  Your HbA1c is above target, your diabetes can be controlled better. Aim for a HbA1c below 7."
                lifestyle = True
            else:
                output_phrase = ":large_green_circle:  Your HbA1c is below 7, which is within expected range for a diabetic."
        if glucose_value >0:
            if glucose_value > 6:
                output_phrase += "  \nYour fasting glucose level is slightly high. Please consult your doctor for your specific glucose targets. Having a HbA1c measurement may be helpful to better evauate your diabetes control."
            else:
                output_phrase += "  \nYour fasting glucose level is within range, <6."
    else:
        #diagnose dm
        if a1c_value >= 6.5 or glucose_value >= 7:
            output_phrase = ":large_orange_circle:  You likely have diabetes. Consult a doctor for advice, you may need to be started on medications."
            lifestyle = True
        elif a1c_value >= 6.1 or glucose_value >=6.1:
            output_phrase = ":large_yellow_circle:  You likely have prediabetes."
            if a1c_value >= 5.7:
                output_phrase += " Your HbA1c is >6.0." 
            if glucose_value >=5.6:
                output_phrase += " Your fasting glucose is >6.0. If this was a non-fasting sample, it may be difficult to assess. A fasting sample is preferred."
            lifestyle = True
        else:
            output_phrase = ":large_green_circle: You likely do not have diabetes."
    if lifestyle:
        output_phrase += " Eat a healthy balanced diet - using My Healthy Plates (filling a quarter of the plate with wholegrains, quarter with good sources of protein, and half with fruit and vegetables). Maintain a healthy weight BMI ranging from 18.5 to 22.9 kg/m2. Exercise regularly, aiming for 150 minutes of moderate-intensity activity per week or 20 minutes of vigorous-intensity activity 3 or more days a week). Limit alcohol intake to 1 drink per day for females, and 2 drinks per day for males."
    if inputattributes["smoker"]:
        output_phrase += " You are highly encouraged to quit smoking."
    return output_phrase 

#print(f"advice {get_dm_advice(test_attributes, testdict)}")
