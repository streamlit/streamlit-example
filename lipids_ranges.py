import json


# Open the file containing the JSON data
with open('Sample json extraction\sample json extraction.txt') as f:
    # Load the JSON data from the file
    data = json.load(f)

# add data to a dictionary where key is test name and value is dictionary of test name/results etc. 
masterdict = {}
# Access each individual object and list the attributes
for dict in data['test_results']:
    masterdict [dict["test_name"]] = dict

testdict = {
  "CHOLESTEROL":
    {
      "test_name": "CHOLESTEROL",
      "test_value": 5.1,
      "test_ref_min": "NA",
      "test_ref_max": "NA",
      "test_unit": "mmol/l"
    },
    "HDL CHOLESTEROL":
    {
      "test_name": "HDL CHOLESTEROL",
      "test_value": 1.6,
      "test_ref_min": "NA",
      "test_ref_max": "NA",
      "test_unit": "mmol/l"
    }
}


#access value by e.g. masterdict["CHOLESTEROL"]["test_value"]
#print (f"master dict {masterdict}")

#sample of attributes needed
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

def getLDLtarget (attributes):
    if(attributes["stroke"]):
        return 1.8
    if(attributes["diabetes"]):
        return 2.6
    if(attributes["heart_attack"]):
        return 1.4
    #SGFRS scoring, only if no stroke or diabetes then proceed 
    LDLtarget = 0
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
    print (f"scoring now") 
    score = 0
    sex = 0 if attributes["sex"] == "male" else 1
    age = attributes["age"]
    tcval = attributes ["total_cholesterol"]["test_value"]
    if attributes ["total_cholesterol"]["test_unit"].lower() =="mg/dl":
        if tcval > 280: cholbracket = 3
        elif tcval > 240: cholbracket = 2
        elif tcval > 200: cholbracket = 1
        elif tcval > 160: cholbracket = 0
        else: cholbracket = -1 
    elif attributes ["total_cholesterol"]["test_unit"].lower() =="mmol/l":
        if tcval > 7.2: cholbracket = 3
        elif tcval > 6.1: cholbracket = 2
        elif tcval > 5.1: cholbracket = 1
        elif tcval > 4.1: cholbracket = 0
        else: cholbracket = -1 
    else: 
        cholbracket = -1
        print ("invalid cholesterol units")

    hval = attributes ["hdl_cholesterol"]["test_value"]
    if attributes ["hdl_cholesterol"]["test_unit"].lower() =="mg/dl":
        if hval > 59: hdlbracket = 0
        elif hval > 49: hdlbracket = 1
        elif hval > 40: hdlbracket = 2
        else: hdlbracket = 3
    if attributes ["hdl_cholesterol"]["test_unit"].lower() =="mmol/l":
        if hval > 1.5: hdlbracket = 0
        elif hval > 1.2: hdlbracket = 1
        elif hval > 1: hdlbracket = 2
        else: hdlbracket = 3
    else: 
        hdlbracket = -1
        print ("invalid cholesterol units")

    bval = attributes ["systolic_blood_pressure"]
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
        print ("you are too young to use this calculator")
        return 0

    # age only points
    agescore += curdict["age"][agebracket][sex] 
    print (f"agescore {agescore} after age only")

    # age and cholesterol points
    if cholbracket > -1: #no points if cholesterol is <4.1 
        agescore += curdict["tchol"][cholbracket][sex]
        print (f"agescore {agescore} after chol")

    # age and smoking points 
    if attributes["smoker"]:
        agescore += curdict["smoker"][sex]
        print (f"agescore {agescore} after smoking")

    score += agescore

        
    print (f"score {score}") 
    return LDLtarget

LDLtarget = getLDLtarget (test_attributes)
print (f"LDL target {LDLtarget}") 
