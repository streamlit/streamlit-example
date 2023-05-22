import streamlit as st
import sass
import math
from datetime import date
import base64


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

from pages.payopt_tools.ps_tools import set_png_as_top_rhs_logo
set_png_as_top_rhs_logo()


# ========================================================================================================



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
