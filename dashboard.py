import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit.logger import get_logger

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
    weeks = np.array([i for i in range(1, 12)])
    
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


  # Function to draw the plots
  def draw_plot(indicator):
      weeks, data = generate_data(indicator)
      fig = go.Figure()
      fig.add_trace(go.Scatter(x=weeks, y=data, mode='lines+markers'))
      fig.update_layout(title=indicator, margin=dict(t=20, b=20, l=30, r=30), height=150, font=dict(size=10), title_font=dict(size=12))
      return fig

  # Main application
  industries = ["Overall economy", "Agriculture", "Construction", "Manufacturing", "Retail", "Health/social sector", "Retail / Wholesale", "Education", "Transportation and storage"]

  selected_industry = st.sidebar.selectbox('Select Industry:', industries, 0)

  st.title(f"Dashboard for {selected_industry}")

  indicators_grouped = [
      ["GDP", "Indicator: FDI inflows", "Unemployment rate"],
      ["PMI", "Interest rate", "Levels of wages"],
      ["Foreign trade", "Stock market volatility (VIX)", "CPI (core? Or inflation?)"],
      ["Placeholder for an SMB indicator", "Loans defaults/Nonperforming loans to total loans", "Personal consumption spending"]
  ]

  for group in indicators_grouped:
      col1, col2, col3 = st.columns(3)
      with col1:
          st.plotly_chart(draw_plot(group[0]), use_container_width=True)
      with col2:
          st.plotly_chart(draw_plot(group[1]), use_container_width=True)
      with col3:
          st.plotly_chart(draw_plot(group[2]), use_container_width=True)

if __name__ == '__main__':
    run()

