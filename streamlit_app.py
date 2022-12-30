import io
import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions


@st.cache(allow_output_mutation=True)
def load_model():
    return EfficientNetB0(weights="imagenet")


def main():

    st.title("Image classifications")
    st.markdown("## Image recognition - using `tensorflow`, `streamlit` ")

    def preprocess_image(img):
        img = img.resize((224, 224))
        num = image.img_to_array(img)
        num = np.expand_dims(num, axis=0)
        num = preprocess_input(num)
        return num

    def load_image():
        uploaded_file = st.file_uploader(label="Choose an image for recognition")
        if uploaded_file is not None:
            image_data = uploaded_file.getvalue()
            st.image(image_data)
            return Image.open(io.BytesIO(image_data))
        else:
            return None

    def print_predictions(pred):
        classes = decode_predictions(pred, top=3)[0]
        for cl in classes:
            st.write(cl[1], cl[2])

    model = load_model()

    img = load_image()
    result = st.button("Recognize Image")
    if result:
        num = preprocess_image(img)
        pred = model.predict(num)
        st.write("Recognition results:")
        print_predictions(pred)
    else:
        st.error("Choose an image!")


if __name__ == "__main__":
    main()
