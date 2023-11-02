import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit.logger import get_logger
import hashlib

LOGGER = get_logger(__name__)

def run():
    st.markdown("""
        <style>
            .st-emotion-cache-1y4p8pa {
                flex: 1 1 0%;
                width: 100%;
                padding: 6rem 1rem 10rem;
                max-width: 100rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Generate random data for each indicator
    def generate_data(indicator):
        weeks = np.array([i for i in range(23, 36)])

        if indicator == "GDP":
            data = np.linspace(350, 400, 11)  # Simulate steady growth
        elif indicator == "Indicator: FDI inflows":
            data = np.random.uniform(200, 400, 11)  # Fluctuating values
        elif indicator == "Unemployment rate":
            data = np.random.uniform(4, 7, 11)  # Unemployment rates
        elif indicator == "PMI":
            data = np.random.uniform(45, 55, 11)  # PMI values
        elif indicator == "Interest rate":
            data = np.random.uniform(0.1, 3, 11)  # Interest rates
        elif indicator == "Levels of wages":
            data = np.linspace(2000, 3000, 11)  # Wages increasing
        elif indicator == "Foreign trade":
            data = np.random.uniform(-500, 500, 11)  # Trade balance
        elif indicator == "Stock market volatility (VIX)":
            data = np.random.uniform(10, 60, 11)  # VIX
        elif indicator == "CPI (core? Or inflation?)":
            data = np.random.uniform(0, 5, 11)  # CPI or inflation
        elif indicator == "Placeholder for an SMB indicator":
            data = np.random.randint(100, 200, 11)  # Placeholder SMB values
        elif indicator == "Loans defaults/Nonperforming loans to total loans":
            data = np.random.uniform(0, 10, 11)  # Loan defaults
        elif indicator == "Personal consumption spending":
            data = np.linspace(1000, 2000, 11)  # Consumption spending trend

        return weeks, data

    indicator_units = {
        "GDP": " (Billions USD)",
        "Indicator: FDI inflows": " (Millions USD)",
        "Unemployment rate": " (%)",
        "PMI": " (Index)",
        "Interest rate": " (%)",
        "Levels of wages": " (USD)",
        "Foreign trade": " (Millions USD)",
        "Stock market volatility (VIX)": " (Index Points)",
        "CPI (core? Or inflation?)": " (%)",
        "Placeholder for an SMB indicator": " (Index Points)",
        "Loans defaults/Nonperforming loans to total loans": " (%)",
        "Personal consumption spending": " (Billions USD)"
    }

    def draw_plot(title, detailed=False):
        weeks, data = generate_data(indicator=title)

        # Create the figure
        fig = go.Figure()

        # Check if a detailed view is requested
        if detailed and title in indicator_units:  # Making sure the detailed view is only for the main indicators
            # Display the larger plot without annotations for growth rate
            fig.add_trace(go.Scatter(x=weeks, y=data, mode='lines+markers', name=title))
            fig.update_layout(margin=dict(t=20, b=20, l=30, r=30), height=300)
        else:
            # Display the regular plot
            fig.add_trace(go.Scatter(x=weeks, y=data, mode='lines+markers'))
            fig.update_layout(title=f"{title}{indicator_units.get(title, '')}",
                            margin=dict(t=20, b=20, l=30, r=30),
                            height=150, font=dict(size=10),
                            title_font=dict(size=12))

        return fig
    
    def display_growth_metric(title):
        weeks, data = generate_data(indicator=title)

        if len(data) >= 3:
            # Calculate the difference and percentage change over the last 30 days (approximated to 3 weeks here)
            difference = data[-1] - data[-3]
            growth_rate = ((data[-1] - data[-3]) / data[-3]) * 100
        else:
            difference = 0
            growth_rate = 0

        current_value = data[-1]
        
        growth_icon = "🔺" if difference > 0 else "🔻"  # Change icon based on growth direction
        
        st.metric(label=title + indicator_units.get(title, ''),
                value=f"${current_value:.2f}",
                delta=f"{growth_icon} ${abs(difference):.2f} ({growth_rate:.2f}%) vs previous 3 weeks")
        
    # Main application
    industries = ["Overall economy", "Agriculture", "Construction", "Manufacturing", "Retail", "Health/social sector", "Retail / Wholesale", "Education", "Transportation and storage"]

    selected_industry = st.sidebar.selectbox('Select Industry:', industries, 0)

    # Use the hash of the industry name as the seed
    industry_hash = int(hashlib.sha256(selected_industry.encode('utf-8')).hexdigest(), 16) % (10**8)  # Hash to a number
    np.random.seed(industry_hash)

    st.title(f"Dashboard for {selected_industry}")

    indicators_grouped = [
    ["GDP", "Indicator: FDI inflows", "Unemployment rate"],
    ["PMI", "Interest rate", "Levels of wages"],
    ["Foreign trade", "Stock market volatility (VIX)", "CPI (core? Or inflation?)"],
    ["Placeholder for an SMB indicator", "Loans defaults/Nonperforming loans to total loans", "Personal consumption spending"]
    ]

    # New functions for displaying the main dashboard and resetting the state
    def show_main_dashboard():
        st.title(f"Dashboard for {selected_industry}")

        for group in indicators_grouped:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.plotly_chart(draw_plot(group[0]), use_container_width=True)
            with col2:
                st.plotly_chart(draw_plot(group[1]), use_container_width=True)
            with col3:
                st.plotly_chart(draw_plot(group[2]), use_container_width=True)

        detailed_metric = st.sidebar.selectbox("Select an indicator for a detailed view:", ["None"] + all_indicators, 0)
        if detailed_metric != "None":
            if st.sidebar.button(f"View {detailed_metric} in detail"):
                st.session_state.view_detailed_metric = True
                st.session_state.detailed_metric_name = detailed_metric

    def reset_state():
        st.session_state.view_detailed_metric = False
        show_main_dashboard()

    # Check if the detailed view page is set in the state
    try:
        if st.session_state.view_detailed_metric:
            # If the detailed metric page is set, display it and then reset the flag
            detailed_metric = st.session_state.detailed_metric_name
            display_growth_metric(detailed_metric)
            st.plotly_chart(draw_plot(detailed_metric, detailed=True), use_container_width=True)
            st.button('Go back to dashboard', on_click=reset_state)
        else:
            show_main_dashboard()
    except AttributeError:
        show_main_dashboard()

if __name__ == '__main__':
    run()