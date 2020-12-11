# import streamlit as st
# PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:","layout":"centered"}
# st.beta_set_page_config(**PAGE_CONFIG)


# def main():
# 	st.title("Awesome Streamlit for ML")
# 	st.subheader("How to run streamlit from colab")


# 	menu = ["Home","About"]
# 	choice = st.sidebar.selectbox('Menu',menu)
# 	if choice == 'Home':
# 		st.subheader("Streamlit From Colab")


# if __name__ == '__main__':
# 	main()
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
# from model import get_pose
from measurement_utils import get_measurements
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("Body Pose and Measurement Example")
height = st.text_input("Enter Height", 175)
filename = st.text_input("Enter File Name", 'Zac')
height = int(height)
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"])
get_res = st.button('Get Measurements')
demo = st.button('Show Demo Image')
if (uploaded_file is not None) and get_res:
    # if uploaded_file is not None:

    image = Image.open(uploaded_file)
    # use_column_width=True)
    st.write("")
    st.write("Calculating Measurements...")
    img_array = np.array(image).copy()
    # result, height_r, shoulder_width, waist_width = get_pose(img_array,height)
    result, df, _ = get_measurements(filename, img_array, height=height)
    st.image([img_array, result], width=256)
    st.dataframe(df)

if demo:
    height = 175
    image = Image.open('./images/zac-new.jpeg')
    # use_column_width=True)
    st.write("")
    st.write("Calculating Measurements...")
    img_array = np.array(image).copy()
    # result, height_r, shoulder_width, waist_width = get_pose(img_array,height)
    result, df, _ = get_measurements(filename, img_array, height=height)
    st.image([img_array, result], width=256)
    st.dataframe(df)
    # st.dataframe(pd.DataFrame({"Measurement":["Height","shoulder_width","waist_width"], "Value":[height_r,shoulder_width,waist_width]}))
    # st.write('%s (%.2f%%)' % (label[1], label[2]*100))
