import streamlit as st
import numpy as np
import plotly.graph_objects as go
import hashlib
import numpy as np
import datetime
import toml
import plotly.express as px

# Load configuration from config.toml
with open('config.toml', 'r') as config_file:
    config = toml.load(config_file)

# Extract configurations
indicator_units = config['indicator_units']
industries = config['industries']['names']
indicators_grouped = {key: [group for group in config['indicators_grouped'][key].values()] for key in config['indicators_grouped']}

# Generate random data for each indicator
def generate_data(indicator):
    # Assuming January 1st is the start of week 1 of 2023
    start_date = datetime.date(2023, 1, 1)
    
    # Calculate the date for week 23 (23 weeks * 7 days/week - 7 days since we start from week 1)
    start_week_23 = start_date + datetime.timedelta(weeks=22)  # Python weeks start from 0
    
    # Generate dates for weeks 23 to 35
    dates = [start_week_23 + datetime.timedelta(weeks=i) for i in range(13)]

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
        data = np.random.uniform(0, 10, 11)
    elif indicator == "Personal consumption spending":
        data = np.random.uniform(5, 50, 11)
    elif indicator == "Sales CAGR of industry leaders":
        data = np.random.uniform(0, 20, 11)
    elif indicator == "Net working capital and cash reserves as a percentage of turnover":
        data = np.random.uniform(10, 60, 11)
    elif indicator == "Demand for Labor":
        data = np.random.uniform(50, 150, 11)
    elif indicator == "OpEx CAGR of industry leaders":
        data = np.random.uniform(0, 20, 11)
    elif indicator == "# companies closed / opened":
        data = np.random.randint(-10, 10, 11)
    elif indicator == "Total investments":
        data = np.random.uniform(0, 500, 11)
    else:
        print(f"Unexpected indicator value: {indicator}")
        data = np.array([])  # Default case to ensure `data` is always initialized

    return dates, data

def draw_plot(title, detailed=False):
    dates, data = generate_data(indicator=title)

    # Create the figure
    fig = go.Figure()

    # Check if a detailed view is requested
    if detailed and title in indicator_units:  # Making sure the detailed view is only for the main indicators
        # Display the larger plot without annotations for growth rate
        fig.add_trace(go.Scatter(x=dates, y=data, mode='lines+markers', name=title))
        fig.update_layout(margin=dict(t=20, b=20, l=30, r=30), height=300)
    else:
        # Display the regular plot
        fig.add_trace(go.Scatter(x=dates, y=data, mode='lines+markers'))
        fig.update_layout(title=f"{title}{indicator_units.get(title, '')}",
                        margin=dict(t=20, b=20, l=30, r=30),
                        height=150, font=dict(size=10),
                        title_font=dict(size=12))

    return fig

def display_growth_metric(title):
    dates, data = generate_data(indicator=title)

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

def get_industry_hash(selected_industry):
    return int(hashlib.sha256(selected_industry.encode('utf-8')).hexdigest(), 16) % (10**8)
