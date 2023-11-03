import streamlit as st
import numpy as np
from utils import generate_data, draw_plot, display_growth_metric, get_industry_hash
from utils import indicator_units, industries, indicators_grouped

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

    # Set the title of the tab
    st.set_page_config(page_title="JDC Dashboard")

    # New functions for displaying the main dashboard and resetting the state
    def show_main_dashboard(selected_industry, indicators_grouped):
        industry_specific_indicators = indicators_grouped[selected_industry]
        
        # Check if the industry has any indicators
        if not industry_specific_indicators:
            st.title(f"{selected_industry} Dashboard")
            st.write("Under construction!")
            return

        st.title(f"Dashboard for {selected_industry}")

        for group in industry_specific_indicators:
            col1, col2, col3 = st.columns(3)
            if group[0]:
                with col1:
                    st.plotly_chart(draw_plot(group[0]), use_container_width=True)
            if len(group) > 1 and group[1]:
                with col2:
                    st.plotly_chart(draw_plot(group[1]), use_container_width=True)
            if len(group) > 2 and group[2]:
                with col3:
                    st.plotly_chart(draw_plot(group[2]), use_container_width=True)
        
        # Flatten the list of indicators
        all_indicators = [indicator for group in industry_specific_indicators for indicator in group]

        industry_specific_indicators_flat = [indicator for group in indicators_grouped[selected_industry] for indicator in group]
        detailed_metric = st.sidebar.selectbox("Select an indicator for a detailed view:", ["None"] + industry_specific_indicators_flat, 0)

        if detailed_metric != "None":
            if st.sidebar.button(f"View {detailed_metric} in detail", key='view_detail'):
                st.session_state['view_detailed_metric'] = True
                st.session_state['detailed_metric_name'] = detailed_metric
                # Force a rerun after updating the session state
                st.rerun()

    if st.session_state.get('view_detailed_metric', False):
        detailed_metric = st.session_state.get('detailed_metric_name', '')
        display_growth_metric(detailed_metric)
        st.plotly_chart(draw_plot(detailed_metric, detailed=True), use_container_width=True)
        
        if st.button('Go back to dashboard', key='back_dashboard'):
            # Explicitly changing the state and immediately using this information
            st.session_state['view_detailed_metric'] = False
    else:
        selected_industry = st.sidebar.selectbox('Select Industry:', industries, 0)
        industry_hash = get_industry_hash(selected_industry)
        np.random.seed(industry_hash)
        show_main_dashboard(selected_industry, indicators_grouped)

if __name__ == '__main__':
    run()
