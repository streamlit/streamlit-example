# import streamlit as st

# # Assuming you have a function that takes an image and returns similar image IDs
# def get_similar_images(image):
#     # Your similarity model logic here
#     similar_image_ids = your_model(image)
#     return similar_image_ids

# # Assuming you have a function that retrieves the images based on their IDs
# def get_image_by_id(image_id):
#     # Your image retrieval logic here
#     image = your_image_retrieval_function(image_id)
#     return image

# def main():
#     st.title("Image Similarity Search")

#     uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

#     if uploaded_image is not None:
#         # Process the uploaded image and get similar image IDs
#         similar_image_ids = get_similar_images(uploaded_image)

#         st.write(f"Found {len(similar_image_ids)} similar images.")

#         images_per_page = 20
#         num_pages = (len(similar_image_ids) + images_per_page - 1) // images_per_page

#         page_num = st.slider("Select Page", min_value=1, max_value=num_pages)

#         start_idx = (page_num - 1) * images_per_page
#         end_idx = min(start_idx + images_per_page, len(similar_image_ids))

#         for i in range(start_idx, end_idx):
#             similar_image_id = similar_image_ids[i]
#             similar_image = get_image_by_id(similar_image_id)
#             st.image(similar_image, caption=f"Similar Image {i+1}", use_column_width=True)

# if __name__ == "__main__":
#     main()












from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    
    total_points = st.slider("Number of points in spiral HAAAAA", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
