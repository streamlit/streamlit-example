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

st.set_page_config(layout="wide")
dataframe = None  # main dataframe of information (global scope)

if "halt_process" not in st.session_state:
    st.session_state.halt_process = True

crs_options = ['EPSG:7846', 'EPSG:7848', 'EPSG:7850', 'EPSG:7852', 'EPSG:7854', 'EPSG:7856', 'EPSG:4979']



# Transform
def transform(dataframe):
    pass


def callback_halt_process():
    st.session_state.halt_process = not st.session_state.halt_process


def dataframe_selections(df):
    # df_with_selections = st.data_editor(df.columns.values)
    df_with_selections = pd.DataFrame(df.columns.values)
    df_with_selections.columns = ["Column Headers"]

    df_with_selections.insert(1, "Select All  X Axes (Longitude)", False)
    df_with_selections.insert(2, "Select All Y Axes (Latitude)", False)

    edited_df = st.data_editor(df_with_selections,
                               column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                               width=1000,)

    filtered_for_x = edited_df[edited_df["Select All  X Axes (Longitude)"] == True]
    filtered_x_headers = filtered_for_x["Column Headers"]

    filtered_for_y = edited_df[edited_df["Select All Y Axes (Latitude)"] == True]
    filtered_y_headers = filtered_for_y["Column Headers"]

    return [filtered_x_headers.tolist(),filtered_y_headers.tolist()]


def main():
    st.title("Coordinate Transformation Utility")
    st.text("Upload an Excel or CSV file to convert coordinates into GPS DD(Decimal Degrees)")

    col_size = [5, 1, 5]
    col1, col2, col3 = st.columns(col_size, gap="large")

    with col1:
        st.subheader("Input Coordinates")
        src_crs = st.selectbox("Select the source coordinate system", crs_options, index=5)
        src_crs = pyproj.CRS(src_crs)  # https://epsg.io/7856; GDA2020 / MGA zone 56

        # Create a file uploader widget
        uploaded_file = st.file_uploader("Upload your CSV or Excel file that contains geographic information",
                                         type=["csv", "xlsx", "xls"])

        if uploaded_file is not None:
            # Read the uploaded CSV or Excel file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            units = st.radio("Units", ["m", "mm"])

            # st.dataframe(df, height=200)
            st.subheader("Select the Relevant Column Headers")
            selections = dataframe_selections(df)

    with col3:
        st.subheader("Output Coordinates")
        target_crs = st.selectbox("Select the target coordinate system", crs_options, index=6)
        target_crs = pyproj.CRS(target_crs)  # WGS84; https://epsg.io/4979

    with col2:
        # pad above button with some blank lines
        for i in range(20): st.markdown("")

        # process_button = st.button("Do Stuff! → ", type="primary", key="proc_button",
        #                            disabled=st.session_state.halt_process)

        if st.button(" Translate → ", on_click=callback_halt_process):
            try:  # Streamlit throws errors before the use has even selected the columns they want to use
                points_x = df.loc[:, selections[0]].astype(float)
                points_y = df.loc[:, selections[1]].astype(float)
                if units == "mm":
                    points_x /= 1000.0  # convert mm to m
                    points_y /= 1000.0  # convert mm to m

            except:
                pass

            with col3:
                st.write("X Values", points_x)
                st.write("Y Values", points_y)
                transformer = pyproj.Transformer.from_crs(src_crs, target_crs)  # the transformer
                # test = transformer.transform(points_x, 0)
                # for list in test:
                #     st.write("***list***")
                #     st.write(list)
                #     st.write("***list end***")
                #df['LATITUDE'] = ls_lat
                #df['LONGITUDE'] = ls_lon

                st.subheader("Transformed Data")
                #st.dataframe(df)


    st.subheader("Data upload")
    # Create a file uploader widget
    # uploaded_file = st.file_uploader("Upload your CSV file that contains geographic information", type=["csv"])

    st.subheader("Coordinate frames transformations")
    st.markdown(
        '[EPSG:7856 - GDA2020 / MGA Zone 56](https://epsg.io/7856) | [EPSG:7854 - GDA2020 / MGA Zone 54](https://epsg.io/7854)')
    st.markdown(
        '[EPSG:7852 - GDA2020 / MGA Zone 52](https://epsg.io/7852) | [EPSG:7850 - GDA2020 / MGA Zone 50](https://epsg.io/7850)')
    st.markdown(
        '[EPSG:7848 - GDA2020 / MGA Zone 48](https://epsg.io/7848) | [EPSG:7846 - GDA2020 / MGA Zone 46](https://epsg.io/7846)')
    st.markdown('[EPSG:4979 - WGS84](https://epsg.io/4979)')

    if uploaded_file is not None:
        # Read the uploaded CSV file
        # df = pd.read_csv(uploaded_file)

        # Get the column names from the CSV file
        column_names = df.columns.tolist()

        # Create dropdown menus for latitude and longitude column selection

        y_column = st.selectbox("Select latitude/y-axis data column/header", column_names)
        x_column = st.selectbox("Select longitude/x-axis data column/header", column_names)


        if st.button("Process data"):
            try:  # Streamlit throws errors before the use has even selected the columns they want to use
                points_x = df.loc[:, x_column].astype(float)
                points_y = df.loc[:, y_column].astype(float)
                if units == "mm":
                    points_x /= 1000.0  # convert mm to m
                    points_y /= 1000.0  # convert mm to m
            except:
                pass

            src_crs_1 = pyproj.CRS(src_crs)  # https://epsg.io/7856; GDA2020 / MGA zone 56
            target_crs_1 = pyproj.CRS(target_crs)  # WGS84; https://epsg.io/4979
            transformer = pyproj.Transformer.from_crs(src_crs_1, target_crs_1)  # the transformer

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

    st.image("Zutari_Black Logo_Background transparent_No Safe Space.png", width=50)


if __name__ == "__main__":
    main()
