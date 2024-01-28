test_results = {
	"height":{
		"test_found":False,
		"test_value":1.5,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		},
	"weight":{
		"test_found":False,
		"test_value":70,
		"test_unit":False,
		"test_ref_min":False,
		"test_ref_max":False
		}
}


def bmi_advice(test_results):
    print ("in bmi advice")
    output_string = "I didn't catch that"
    weight = test_results["weight"]["test_value"]
    height = test_results["height"]["test_value"]
    if weight > 0 and height > 0:
        bmi = round(weight / pow(height,2), 1)
    else:
        return ":large_yellow_circle: You need both weight and height to calculate BMI."
    weightloss = False
    if bmi >=27.5: 
        output_string = ":large_orange_circle:  You are obese. Your BMI is " + str(bmi)
        weightloss = True
    elif bmi >= 23:
        output_string = ":large_orange_circle:  You are overweight. Your BMI is " + str(bmi)
        weightloss = True
    elif bmi < 18.5:
        output_string = ":large_orange_circle:  You are underweight. Your BMI is " + str(bmi)+ " Consider increasing food intake, for example, by taking smaller, frequent healthy meals. Increase protein intake by taking more lean meats, fish, eggs, dairy, legumes and nuts. Do strength training to build up muscles."
    else:
        output_string = ":large_green_circle: You have a healthy BMI. Your BMI is " + str(bmi)
    if weightloss:
        output_string += "Choose healthier choices that are lower in fat (e.g. lean meat, low-fat dairy products), lower or no sugar (e.g. unsweetened beverages, fresh fruits), and higher in fibre (e.g. whole-meal bread, brown rice). Look out for alternatives that are lower in calories. Reduce your meal sizes by consuming ¾ of your usual. Do some moderate-intensity aerobic physical activities such as brisk walking, swimming or cycling for a minimum of 150-300 minutes weekly. If you're just starting out, accumulating shorter bouts of 10-minute exercise is a good start too."
    return output_string

#print ("advice " + bmi_advice(test_results))
