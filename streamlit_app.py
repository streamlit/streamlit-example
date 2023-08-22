from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pyproj
import io

# Coordinate transformation utility
# Developed by Andre Broekman
# Last modified: 2023-08-16

dataframe = None  # main dataframe of information (global scope)

print("test")

# Transform
def transform(dataframe):
    pass


def test():
    '''

    :return: None
    '''
    pass

def main():

    st.image("Zutari_Black Logo_Background transparent_No Safe Space.png", width=50)
    st.title("Coordinate Transformation Utility")

    st.subheader("Data upload")
    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload your CSV file that contains geographic information", type=["csv"])

    st.subheader("Coordinate frames transformations")
    st.markdown(
        '[EPSG:7856 - GDA2020 / MGA Zone 56](https://epsg.io/7856) | [EPSG:7854 - GDA2020 / MGA Zone 54](https://epsg.io/7854)')
    st.markdown(
        '[EPSG:7852 - GDA2020 / MGA Zone 52](https://epsg.io/7852) | [EPSG:7850 - GDA2020 / MGA Zone 50](https://epsg.io/7850)')
    st.markdown(
        '[EPSG:7848 - GDA2020 / MGA Zone 48](https://epsg.io/7848) | [EPSG:7846 - GDA2020 / MGA Zone 46](https://epsg.io/7846)')
    st.markdown('[EPSG:4979 - WGS84](https://epsg.io/4979)')
    crs_options = ['EPSG:7846', 'EPSG:7848', 'EPSG:7850', 'EPSG:7852', 'EPSG:7854', 'EPSG:7856', 'EPSG:4979']
    src_crs = st.selectbox("Select the source coordinate system", crs_options)
    target_crs = st.selectbox("Select the target coordinate system", crs_options)

    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Get the column names from the CSV file
        column_names = df.columns.tolist()

        # Create dropdown menus for latitude and longitude column selection

        y_column = st.selectbox("Select latitude/y-axis data column/header", column_names)
        x_column = st.selectbox("Select longitude/x-axis data column/header", column_names)

        units = st.radio("Units",["m", "mm"])

        if st.button("Process data"):
            try:  # Streamlit throws errors before the use has even selected the columns they want to use
                points_x = df.loc[:, x_column].astype(float)
                points_y = df.loc[:, y_column].astype(float)
                if units == "mm":
                    points_x /= 1000.0  # convert mm to m
                    points_y /= 1000.0  # convert mm to m
            except:
                pass

            src_crs = pyproj.CRS(src_crs)  # https://epsg.io/7856; GDA2020 / MGA zone 56
            target_crs = pyproj.CRS(target_crs)  # WGS84; https://epsg.io/4979
            transformer = pyproj.Transformer.from_crs(src_crs, target_crs)  # the transformer

            points_x = points_x.values.tolist()
            points_y = points_y.values.tolist()
            ls_lat, ls_lon = transformer.transform(points_x, points_y)

            df['LATITUDE'] = ls_lat
            df['LONGITUDE'] = ls_lon

            st.subheader("Transformed Data")
            st.dataframe(df)

            if True:
                map_label = st.markdown('Map of the coordinates:')
                st.map(df)
            else:
                map_label = st.markdown('Error occurred when trying to generate a map of the coordinates')

            # Add a button to download the transformed data as CSV
            st.download_button("Download CSV", df.to_csv(index=False), file_name="data.csv")


if __name__ == "__main__":
    main()
