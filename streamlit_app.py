from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pyproj

import io

# Coordinate transformation utility
# Developed by Andre Broekman
# Last edited by Astrid van der Laan
# Last modified: 2023-08-29

st.set_page_config(layout="wide")
dataframe = None  # main dataframe of information (global scope)

if "halt_process" not in st.session_state:
    st.session_state.halt_process = True

crs_options = ['EPSG:7846', 'EPSG:7848', 'EPSG:7850', 'EPSG:7852', 'EPSG:7854', 'EPSG:7856', 'EPSG:4979']


# Transform
def transform(dataframe):
    pass


def callback_halt_process():
    st.session_state.halt_process = False


def dataframe_selections(df):
    # df_with_selections = st.data_editor(df.columns.values)
    df_with_selections = pd.DataFrame(df.columns.values)
    df_with_selections.columns = ["Column Headers"]

    df_with_selections.insert(1, "Select All  X Axes (Longitude)", False)
    df_with_selections.insert(2, "Select All Y Axes (Latitude)", False)

    edited_df = st.data_editor(df_with_selections,
                               column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                               width=1000, )

    filtered_for_x = edited_df[edited_df["Select All  X Axes (Longitude)"] == True]
    filtered_x_headers = filtered_for_x["Column Headers"]

    filtered_for_y = edited_df[edited_df["Select All Y Axes (Latitude)"] == True]
    filtered_y_headers = filtered_for_y["Column Headers"]

    return [filtered_x_headers.tolist(), filtered_y_headers.tolist()]


def main():
    st.image("Zutari_Black Logo_Background transparent_No Safe Space.png", width=50)
    st.title("Coordinate Transformation Utility")
    st.text("Upload an Excel or CSV file to convert coordinates into GPS DD(Decimal Degrees)")

    st.markdown("[EPSG Codes](https://epsg.io/4979)")

    col_size = [5, 1, 5]
    col1, col2, col3 = st.columns(col_size, gap="large")

    with col1:
        st.subheader("Input Coordinates")
        src_crs = st.selectbox("Select the source coordinate system", crs_options, index=5)
        src_crs = pyproj.CRS(src_crs)  # https://epsg.io/7856; GDA2020 / MGA zone 56

        # Create a file uploader widget
        uploaded_file = st.file_uploader("Upload your CSV or Excel file that contains geographic information",
                                         type=["csv", "xlsx", "xls"], on_change=callback_halt_process)

        if uploaded_file is not None:
            # Read the uploaded CSV or Excel file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            units = st.radio("Units", ["m", "mm"])

            x_search = df.columns.str.endswith('X')
            y_search = df.columns.str.endswith('Y')

            st.write("X Values", df.loc[:, x_search])
            st.write("Y Values", df.loc[:, y_search])

            columns_x = df.columns[x_search]
            columns_y = df.columns[y_search]

    with col3:
        st.subheader("Output Coordinates")
        target_crs = st.selectbox("Select the target coordinate system", crs_options, index=6)
        target_crs = pyproj.CRS(target_crs)  # WGS84; https://epsg.io/4979

    with col2:
        # pad above button with some blank lines
        for i in range(20): st.markdown("")

        if st.button(" Translate → ", disabled=st.session_state.halt_process):
            try:  # Streamlit throws errors before the use has even selected the columns they want to use
                points_x = df.loc[:, columns_x].astype(float)
                points_y = df.loc[:, columns_y].astype(float)
                if units == "mm":
                    points_x /= 1000.0  # convert mm to m
                    points_y /= 1000.0  # convert mm to m

            except:
                pass

            with col3:
                transformer = pyproj.Transformer.from_crs(src_crs, target_crs)  # the transformer
                map_df = pd.DataFrame()

                for (col_name_x, col_data_x), (col_name_y, col_data_y) in zip(points_x.items(), points_y.items()):
                    ls_lat, ls_lon = transformer.transform(col_data_x.values, col_data_y.values)

                    df[col_name_x+'_LATITUDE'] = ls_lat
                    df[col_name_y+'_LONGITUDE'] = ls_lon

                    map_df['LATITUDE'] = ls_lat
                    map_df['LONGITUDE'] = ls_lon

                x_search = df.columns.str.endswith('LATITUDE')
                y_search = df.columns.str.endswith('LONGITUDE')

                st.write("X Values", df.loc[:, x_search])
                st.write("Y Values", df.loc[:, y_search])

                # Add a button to download the transformed data as CSV
                with col2:
                    st.download_button("Download CSV ↓", df.to_csv(index=False), file_name="converted_gps_data.csv")

                st.markdown('Map of the coordinates')
                st.map(map_df, size=1)








if __name__ == "__main__":
    main()
