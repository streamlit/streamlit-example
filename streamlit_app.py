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
  def generate_data():
      weeks = np.array([i for i in range(1, 12)])
      data = np.random.randint(100, 200, size=(11))
      return weeks, data

  # Function to draw the plots
  def draw_plot(title):
      weeks, data = generate_data()
      fig = go.Figure()
      fig.add_trace(go.Scatter(x=weeks, y=data, mode='lines+markers'))
      fig.update_layout(title=title, margin=dict(t=20, b=20, l=30, r=30), height=150, font=dict(size=10), title_font=dict(size=12))
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

