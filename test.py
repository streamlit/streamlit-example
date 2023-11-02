import requests
import base64

# Specify the path to your image file
image_path = './gallery/abiding-debonair-viper-of-downpour.jpg'  # Replace with the actual path to your image file

# Open and read the image in binary mode
with open(image_path, 'rb') as image_file:
    # Read the image data
    image_data = image_file.read()

# Encode the binary image data to Base64
base64_encoded = base64.b64encode(image_data).decode('utf-8')

# Print or use the base64_encoded string as needed
# print(base64_encoded)

response = requests.post("https://awacke1-image-to-text-salesforce-blip-image-capt-f549b46.hf.space/run/predict", json={
	"data": [
		f"data:image/png;base64,{base64_encoded}",
	]
}).json()

data = response["data"]

print(data)