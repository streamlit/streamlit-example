import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
import base64
import json

def load_image(image_file):
    img = Image.open(image_file)
    return img

def draw_rectangles(image_path, rectangles):
    img = load_image(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for rect_info ,name in zip(rectangles,names):
        xmin = rect_info.get("xmin", 0)
        ymin = rect_info.get("ymin", 0)
        xmax = rect_info.get("xmax", 0)
        ymax = rect_info.get("ymax", 0)
        text = name

        coordinates = (xmin, ymin, xmax, ymax)
        box_width = xmax - xmin



        font_size = int(box_width * 0.16)

        font= ImageFont.truetype("arial.ttf", font_size)

        draw.rectangle(coordinates, outline="red", width=3)

        draw.text((xmin, ymin-70), text, fill="red", font=font)

    return img

st.set_page_config(page_title="OZ Fish", page_icon=":fish:", layout="centered")

"""
# OZ Fish 🐟🐟
"""
image_file = st.file_uploader("Please upload Image/Video")
img_placeholder = st.empty()

if image_file is not None:
    file_details = {"filename": image_file.name, "filetype": image_file.type, "filesize": image_file.size}
    #st.write(file_details)

    img_placeholder.image(load_image(image_file))

    url = "https://yolooo-gvzmtv7baq-ew.a.run.app/"

    # response = requests.get(url).json()

    payload = {"file": image_file.getvalue()}
    post_response = requests.post(url=f"{url}upload/", files=payload)
    post2_response= requests.post(url=f"{url}predict/", files=payload)
    names = post2_response.json()

    rectangles = post_response.json()  # Assuming the response is a JSON array

    if st.button("Analyse Image"):
        st.write('I was clicked 🎉')
        drawn_image = draw_rectangles(image_file, rectangles)
        img_placeholder.image(drawn_image, caption="Image with Rectangles.", use_column_width=True)
    else:
        st.write('I was not clicked 😞')
