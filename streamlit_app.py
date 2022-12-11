import streamlit as st
import cv2

st.title("Satellite Image Diff")

# Upload the first image
image1 = st.file_uploader("Choose the first image")

# Upload the second image
image2 = st.file_uploader("Choose the second image")

# Check if the images have been uploaded
if image1 and image2:
    # Load the images
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    # Check if the images have the same size
    if img1.shape == img2.shape:
        # Calculate the difference between the two images
        diff = cv2.absdiff(img1, img2)

        # Convert the difference image to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Select the area to compare
        area = st.select_area("Select the area to compare")
