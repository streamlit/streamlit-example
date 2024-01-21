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
    "ckd" : False
    "heart_attack" : False ,
    "race" :"indian",
    "systolic_blood_pressure" : 120,
    "on_BP_meds" : False,
    "total_cholesterol" : testdict["total_cholesterol"], #masterdict["CHOLESTEROL"]
    "hdl_cholesterol" : testdict["hdl_cholesterol"] #masterdict["HDL CHOLESTEROL"]
}


def get_dm_advice(inputattributes, inputdict):
    output_phrase = ""
    lifestyle = False
    #known dm
    a1c_value = inputdict["hba1c"]["test_value"]
    glucose_value = inputdict["glucose"]["test_value"]
    targetdict = (8, 6.5, 7)
    if inputattributes["age"] >= 80:
        a1ctarget = 8
    elif inputattributes["age"] <=40:
        a1ctarget = 6.5 
    else:
        a1ctarget = 7.0 
    if a1c_value > a1ctarget:
        output_phrase = "your HbA1c is above target, your diabetes can be controlled better."
        lifestyle = True
    else:
        #diagnose dm
        if a1c_value >= 6.5 or glucose_value >= 7:
            output_phrase = "you have diabetes."
            lifestyle = True
        elif a1c_value >= 5.7 or glucose_value >=5.6:
            output_phrase = "you have prediabetes."
            lifestyle = True
        else:
            output_phrase = "you do not have diabetes."
    if lifestyle:
        output_phrase += "Eat a healthy balanced diet - using My Healthy Plates (filling a quarter of the plate with wholegrains, quarter with good sources of protein, and half with fruit and vegetables). Maintain a healthy weight BMI ranging from 18.5 to 22.9 kg/m2. Exercise regularly, aiming for 150 minutes of moderate-intensity activity per week or 20 minutes of vigorous-intensity activity 3 or more days a week). Limit alcohol intake to 1 drink per day for females, and 2 drinks per day for males."
    if inputattributes["smoker"]:
        output_phrase += "Quit smoking."
    return output_phrase 