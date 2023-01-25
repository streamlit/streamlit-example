import streamlit as st
from PIL import Image

st.set_page_config(page_title="Image Compressor", page_icon=":camera:", layout="wide")

def compress_image(image, size_percentage):
    im = Image.open(image)
    width, height = im.size
    new_width = int(width * size_percentage / 100)
    new_height = int(height * size_percentage / 100)
    im_resized = im.resize((new_width, new_height))
    return im_resized

def main():
    st.title("Image Compressor")
    st.subheader("Upload an image and set the desired size percentage")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        
        st.sidebar.image(image, caption='Original Image', use_column_width=True)
        size_percentage = st.sidebar.slider("Set the image size percentage", min_value=1, max_value=100, value=100)

        compressed_image = compress_image(uploaded_file, size_percentage)
        st.image(compressed_image, caption='Compressed Image', use_column_width=True)
        st.write("Resolution (width, height): ", compressed_image.size)
        if st.button('Download'):
            compressed_image.save(f'compressed_{uploaded_file.name}')
            st.write("Download Compressed Image", file_downloader=True, filename=f'compressed_{uploaded_file.name}')


if __name__ == "__main__":
    main()
