from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pyproj
import io

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

"""
# Import libraries
import pyproj  # https://pyproj4.github.io/pyproj/stable/examples.html
import pandas as pd
from time import time

start_time = time()
df = pd.read_csv('MN01 PANEL COORDINATES.csv')
print('Imported data')
points_x = df.loc[:, 'Coordinates - Survey: Point_X']
points_y = df.loc[:, 'Coordinates - Survey: Point_Y']
points_x /= 1000.0  # convert mm to m
points_y /= 1000.0  # convert mm to m

src_crs = pyproj.CRS('EPSG:7856')  # https://epsg.io/7856; GDA2020 / MGA zone 56
target_crs = pyproj.CRS('EPSG:4979')  # WGS84; https://epsg.io/4979
transformer = pyproj.Transformer.from_crs(src_crs, target_crs)  # the transformer

points_x = points_x.values.tolist()
points_y = points_y.values.tolist()
ls_lon, ls_lat = transformer.transform(points_x, points_y)
print('Completed transformations')

# Assign new columns to the DataFrame
df['Latitude'] = ls_lat
df['Longitude'] = ls_lon

# Save DataFrame to csv file
df.to_csv('test_output.csv')
print('Exported data to CSV')
delta_time = time() - start_time
print('Completed script in %.3f seconds' % delta_time)
"""

def main():
    st.title("GPS Data Tool")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        df = pd.read_csv(uploaded_file)

        # Get the column names from the CSV file
        column_names = df.columns.tolist()

        # Create dropdown menus for latitude and longitude column selection
        latitude_column = st.selectbox("Select Latitude Column", column_names)
        longitude_column = st.selectbox("Select Longitude Column", column_names)

        points_x = df.loc[:, longitude_column]
        points_y = df.loc[:, latitude_column]
        points_x /= 1000.0  # convert mm to m
        points_y /= 1000.0  # convert mm to m

        src_crs = pyproj.CRS('EPSG:7856')  # https://epsg.io/7856; GDA2020 / MGA zone 56
        target_crs = pyproj.CRS('EPSG:4979')  # WGS84; https://epsg.io/4979
        transformer = pyproj.Transformer.from_crs(src_crs, target_crs)  # the transformer

        points_x = points_x.values.tolist()
        points_y = points_y.values.tolist()
        ls_lon, ls_lat = transformer.transform(points_x, points_y)

        df['Latitude'] = ls_lat
        df['Longitude'] = ls_lon

        # Perform your calculations on df (modify this part according to your calculations)
        # Example: df['new_column'] = df['old_column'] * 2

        st.subheader("Transformed Data")
        st.dataframe(df)

        # Add a button to download the transformed data as CSV
        if st.button("Download Transformed CSV"):
            # Create a downloadable link without using base64
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            st.download_button(
                label="Download Transformed CSV",
                data=output,
                file_name="transformed_data.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

