import streamlit as st
import math
from datetime import date, datetime, timezone
import base64


#########################################################################################################################
# Layout and Previse look and feel

# getting the image file for the logo - encoding it ourselves because streamlit is really blurring it too much...
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# here is where the logo magic happens
def set_png_as_top_rhs_logo(png_file = "./logo_title.png"):
# Load the compiled CSS
    with open("./mystyle.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    bin_str = get_base64_of_bin_file(png_file)
    footer_bg_img = """
                <style>
                .css-1dp5vir { 
                    position: absolute;
                    top: 0px;
                    right: 0px;
                    left: 0px;
                    height: 0.125rem;
                    background-image: linear-gradient(90deg, #fedb00, #fedb00);
                    z-index: 999990;
                }
                footer { 
                   visibility: hidden;
                }
                header{ 
                    padding: 0.4rem;
                }
                header:after {
                    display: block;
                    content: "";
                    width: 94%%;
                    height: 80%%;
                    position: absolute;
                    background-image: url("data:image/png;base64,%s");
                    background-position-x: 100%%;
                    background-position-y: 0%%;
                    background-repeat: no-repeat;
                    background-size: contain;
                    background_attachment: fixed;
                    }
                </style>
                """ % bin_str
    st.markdown(footer_bg_img, unsafe_allow_html=True)


# configuring the page and menu items
st.set_page_config(
    page_title="The Previse supplier categorisation tool",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://previ.se',
        'Report a bug': "https://previ.se",
        'About': "(c) 2023 Previse Ltd."
    }
)


# ========================================================================================================

set_png_as_top_rhs_logo()

ref_date = date.fromisoformat('2023-02-10')

KPIs = {
    "Reference Date" : ref_date.isoformat(),
    "Total Payables outstanding" :	"{:,}".format(767462641),
    "Total transaction costs":	"{:,}".format(1840107),
    "Average Working Capital":	"{:,}".format(154159060),
    "DSO" :	10 
}

# Define the main function to run the app
def main():
    # Set the app title
    st.title("Payment Strategy Optimiser")

    st.header("KPIs")
    # Calculate the number of rows needed to display all the KPIs
    num_rows = math.ceil(len(KPIs) / 3)

    # Create a Streamlit column layout for each row
    cols = [st.columns(3) for _ in range(num_rows)]

    # Iterate over the KPIs and add them to the columns
    for i, (kpi_name, kpi_value) in enumerate(KPIs.items()):
        row_idx = i // 3
        col_idx = i % 3
        kpi_col = cols[row_idx][col_idx]
        
        # Add the KPI as a Streamlit metric to the column
        kpi_col.metric(kpi_name, kpi_value)
# Run the app
if __name__ == "__main__":
    main()
