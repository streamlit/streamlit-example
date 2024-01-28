#REMEMBER TO CHANGE BP TO TESTVALS
# import json

# # Open the file containing the JSON data
# with open('Sample json extraction\sample json extraction.txt') as f:
#     # Load the JSON data from the file
#     data = json.load(f)

# # add data to a dictionary where key is test name and value is dictionary of test name/results etc. 
# masterdict = {}
# # Access each individual object and list the attributes
# for dict in data['test_results']:
#     masterdict [dict["test_name"]] = dict

testdict = {
	"ldl_cholesterol": {
		"test_found":True,
		"test_value":5.8,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"hdl_cholesterol": {
		"test_found":True,
		"test_value":1.0,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"total_cholesterol": {
		"test_found":True,
		"test_value":4.1,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
    "systolic_bp":{
		"test_found":True,
		"test_value":200,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"diastolic_bp":{
		"test_found":True,
		"test_value":100,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
}


#access value by e.g. masterdict["CHOLESTEROL"]["test_value"]
#print (f"master dict {masterdict}")

#sample of attributes needed
test_attributes = {
    "age" : 40, 
    "sex" :"male", #0 for male, 1 for female 
    "smoker" : True, 
    "stroke" : False,
    "diabetes" : False ,
    "ckd" : False,
    "heart_attack" : False ,
    "race" :"indian",
    "on_BP_meds" : False,
    "systolic_blood_pressure": 120
}

def getLDLBPtarget (attributes,testvals):
    print ("in ldl target")
    LDLtargetcalc = 0 
    BP_target = (0, 0)
    # check all attributes present else return "invalid"
    if testvals["systolic_bp"]["test_found"]:
        bval = testvals ["systolic_bp"]["test_value"] 
    elif attributes["systolic_blood_pressure"] and  attributes["systolic_blood_pressure"] > 0 :
        bval = attributes["systolic_blood_pressure"]
    else:
        bval = 0
    if(attributes["stroke"]):
        LDLtargetcalc = 1.8
        BP_target = (140, 90) #with disclaimer
    if(attributes["diabetes"] or attributes["ckd"]):
        BP_target = (130, 80) 
        if (attributes["diabetes"] and attributes["ckd"]):
            LDLtargetcalc = 1.8
        else:
            LDLtargetcalc = 2.6
    if(attributes["heart_attack"]):
        LDLtargetcalc = 1.4
        BP_target = (130, 80)   
    #SGFRS scoring, only if no stroke or diabetes then proceed 
    if LDLtargetcalc == 0:
        #function "all" returns true if no values are false (0 values map to false) i.e. if any of these are 0 or empty, return
        if not all ((bval, attributes["age"], attributes["sex"], attributes["race"], testvals["total_cholesterol"]["test_value"], testvals ["hdl_cholesterol"]["test_value"])):
            print ("something missing "+str((bval, attributes["age"], attributes["sex"], attributes["race"], testvals["total_cholesterol"]["test_value"], testvals ["hdl_cholesterol"]["test_value"])))
            print(bool(bval), bool(attributes["age"]), bool (attributes["sex"]), bool(attributes["race"]), bool(testvals["total_cholesterol"]["test_value"]), bool(testvals ["hdl_cholesterol"]["test_value"]))
            return ":large_yellow_circle: More information is needed to calculate your blood pressure or cholesterol target. Please fill in the boxes above (age, sex, race, systolic blood pressure). We also need your HDL cholesterol and total cholesterol. In general, aim for BP <140/90 and LDL <3.4 if you have no other risk factors."
        #dictionary with the values (M, F), corresponding to lower bound of age e.g. 20-40 would be 20
        # first sieve out all 20-40, then split into 20-34 and 35-39 for age score, and total chol for chol score 
        # age as tuple (-9, -7,-4, -3): 20-34 M -9 F -7, 35-39 M -4 F -3 ; 
        # total chol as tuple ((4, 4), (7, 8), (9, 11), (11, 13)) for 4.1-5.1 : M 4 F 4, 5.2-6.1 : M 7 F 8, 6.2-7.2 : M 9 F 11, >7.3 : M 11 F 13
        
        agedict = {
            20 : {
                "age": (
                    (-9, -7), #20-34 (M, F)
                    (-4, -3)), #35-39 (M, F))
                "tchol": (
                    (4, 4), #4.1-5.1 (M, F)
                    (7, 8), #5.2-6.1 (M, F)
                    (9, 11), #6.2-7.2 (M, F)
                    (11, 13)),#>=7.3 (M, F)
                "smoker": (8, 9)
            },
            40 :{
                "age": ((
                    0, 0), 
                    (3, 3)),
                "tchol" : (
                    (3, 3), 
                    (5, 6), 
                    (6, 8), 
                    (8, 10)),
                    "smoker": (5, 7)
            },
            50 :{
                "age": (
                    (6, 6), 
                    (8, 8)),
                "tchol" : (
                    (2, 2), 
                    (3, 4), 
                    (4, 5), 
                    (5, 7)),
                "smoker": (3, 4)
            },
            60 :{
                "age": (
                    (10, 10), 
                    (11, 12)),
                "tchol" : (
                    (1, 1), 
                    (1, 2), 
                    (2, 3), 
                    (3, 4)), 
                "smoker": (1, 2)
            },
            70 :{
                "age": (
                    (12, 14), 
                    (13, 16)),
                "tchol" : (
                    (0, 1), 
                    (0, 1), 
                    (1, 2), 
                    (1, 2)), 
                "smoker": (1, 1)
            }
        }
        #dictionary corresponding to ageless variables 
        otherriskdict = {
            "hdl" : (-1, 0, 1, 2), #regardless of gender, for ranges >=1.6, 1.3-1.5, 1.0-1.2, <1.0
            "sysBP" : (
                ((0, 1),(1, 3)), #untreated M, F , treated M, F for 120-129 
                ((1, 2),(2, 4)), #130-139
                ((1, 3),(2, 5)), #140-159
                ((2, 4),(3, 6)), #>160
            )
        }
        #start scoring 
        #print (f"scoring now") 
        score = 0
        sex = 0 if attributes["sex"].lower() == "male" else 1
        age = attributes["age"]
        tcval = testvals ["total_cholesterol"]["test_value"]
        if testvals ["total_cholesterol"]["test_unit"].lower() =="mg/dl":
            tcval *=  0.02586
            testvals ["total_cholesterol"]["test_value"] *= 0.02586
            testvals ["total_cholesterol"]["test_unit"] = "mmol/L"
        if testvals ["total_cholesterol"]["test_unit"].lower() =="mmol/l":
            if tcval > 7.2: cholbracket = 3
            elif tcval > 6.1: cholbracket = 2
            elif tcval > 5.1: cholbracket = 1
            elif tcval > 4.1: cholbracket = 0
            else: cholbracket = -1 
        else: 
            cholbracket = -1
            return "invalid cholesterol units"

        hval = testvals ["hdl_cholesterol"]["test_value"]
        if testvals ["hdl_cholesterol"]["test_unit"].lower() =="mg/dl":
            hval *=  0.02586
            testvals ["hdl_cholesterol"]["test_value"] *= 0.02586
            testvals ["hdl_cholesterol"]["test_unit"] = "mmol/L"
        if testvals ["hdl_cholesterol"]["test_unit"].lower() =="mmol/l":
            if hval > 1.5: hdlbracket = 0
            elif hval > 1.2: hdlbracket = 1
            elif hval > 1: hdlbracket = 2
            else: hdlbracket = 3
        else: 
            hdlbracket = -1
            return "invalid cholesterol units"

        if bval > 159: bpbracket = 3
        elif bval > 139: bpbracket = 2
        elif bval > 129: bpbracket = 1
        elif bval > 119: bpbracket = 0
        else: bpbracket = -1 

        # HDL points 
        if hdlbracket >-1:
            score += otherriskdict["hdl"][hdlbracket]

        #systolic BP points
        treated = 1 if attributes["on_BP_meds"] else 0
        if bpbracket > -1:
            score += otherriskdict["sysBP"][bpbracket][treated][sex]
        print (f"score after BP/hdl {score}")
        agescore = 0
        if age >70:
            curdict = agedict[70]
            agebracket = 0 if age <75 else 1
            if age >80:
                BP_target = (150, 90) 
        elif age >60:
            curdict = agedict[60]
            agebracket = 0 if age <65 else 1     
        elif age >50:
            curdict = agedict[50]
            agebracket = 0 if age <55 else 1  
        elif age >40:
            curdict = agedict[40]
            agebracket = 0 if age <45 else 1  
        elif age >20:
            curdict = agedict[20]
            agebracket = 0 if age <35 else 1  
        else: 
            return ":large_yellow_circle: You are too young to use this calculator. In general, aim for BP <140/90 and LDL cholesterol < 3.4."

        # age only points
        agescore += curdict["age"][agebracket][sex] 
        #print (f"agescore {agescore} after age only")

        # age and cholesterol points
        if cholbracket > -1: #no points if cholesterol is <4.1 
            agescore += curdict["tchol"][cholbracket][sex]
            #print (f"agescore {agescore} after chol")

        # age and smoking points 
        if attributes["smoker"]:
            agescore += curdict["smoker"][sex]
            #print (f"agescore {agescore} after smoking")

        score += agescore
        if attributes["race"].lower() == "indian":
            raceint = 0
        elif attributes["race"].lower() == "malay":
            raceint = 1
        elif attributes["race"].lower() == "chinese":
            raceint = 2
        else:
            return ":large_yellow_circle: This calculator is not validated for other races. In general, aim for LDL cholesterol <3.4 and BP <140/90."

    #matching to cardiovascular risk bracket 
        cvriskdict = {
            ">20": ((16, 24), (17, 25), (19, 27)), 
            "10-20": ((12, 20), (14, 22), (16, 24)),
            "5-10": ((9, 18), (11, 19), (13, 21)),
            "<5": ((8, 17), (10, 18), (12, 20)),
        }
        recmeds = True
        BP_target = (140,90)
        if score >= cvriskdict[">20"][raceint][sex]:
            LDLtargetcalc = 1.8
            BP_target = (130, 80)
        elif score >= cvriskdict["10-20"][raceint][sex]:
            LDLtargetcalc = 2.6
        elif score >= cvriskdict["5-10"][raceint][sex]:
            LDLtargetcalc = 3.4
        elif score <= cvriskdict["<5"][raceint][sex]:
            LDLtargetcalc = 3.4
            recmeds = False
        
    #print (f"score {score} LDL target {LDLtargetcalc}") 
    if not testvals ["ldl_cholesterol"]["test_found"]:
        return ":large_yellow_circle: LDL cholesterol not found. LDL cholesterol is the main cholesterol that affects medical management."
    if testvals ["ldl_cholesterol"]["test_unit"].lower() =="mg/dl":
        testvals ["ldl_cholesterol"]["test_value"] *= 0.02586
        testvals ["ldl_cholesterol"]["test_unit"] = "mmol/L"
    if testvals ["ldl_cholesterol"]["test_value"] > LDLtargetcalc:
        output_phrase = ":large_orange_circle: Your LDL cholesterol is high. Eat a healthy balanced diet - using My Healthy Plates (filling a quarter of the plate with wholegrains, quarter with good sources of protein (fish, lean meat, tofu and other bean products, nuts), and half with fruit and vegetables. increase soluble fibre intake, avoid food with trans fat,replace saturated fat with polyunsaturated fats. Certain diets like ketogenic diet increase LDL-C levels. Aim for regular moderate-intensity physical activity for 150-300min a week. For people who are overweight or obese, weight reduction of 5–10% could be beneficial for improving lipid profile. Limit alcohol intake to 1 drink per day for females, and 2 drinks per day for males."
        if recmeds:
            output_phrase +=  "You may require cholesterol lowering medications, consult your doctor. "

    else:
        output_phrase = ":large_green_circle: Your LDL cholesterol is within target range (less than " + str(LDLtargetcalc) + ")."
    if testvals["systolic_bp"]["test_found"]:
        bp = (testvals["systolic_bp"]["test_value"], testvals["diastolic_bp"]["test_value"])
        if bp[0] > BP_target[0] or bp[1] > BP_target[1]:
            if bp[0] > 180 or bp[1] > 120:
                output_phrase += "  \n:large_orange_circle: Your blood pressure is dangerously high, SBP >180 or DBP >120. Visit a doctor for assessment.\n"
            else:
                output_phrase += "  \n:large_orange_circle: Your blood pressure is high. Your target should be " + str(BP_target[0]) + "/" + str(BP_target[1]) + " . Take a healthy diet (e.g., reducing salt intake and alcohol consumption), increase physical activity, lose weight if overweight or obese."
            if attributes["stroke"]:
                output_phrase += "Since you have had a stroke before, your blood pressure targets may need to be customised according to the type of stroke. Seek advice from your stroke doctor for specific blood pressure targets."
        else:
            output_phrase += ":large_green_circle: Your BP is in the normal range (less than "+ str(BP_target[0]) + "/" + str(BP_target[1]) + ")."
    if attributes["smoker"]:
        output_phrase += "  \nYou are highly encouraged to quit smoking."
    return output_phrase

#print (f"advice is {getLDLBPtarget (test_attributes, testdict)}")
