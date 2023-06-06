import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to our first App")
    st.sidebar.success("Select pages")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select the page from the dropdown on the left** to EDA, Dataviz, Modelling 
        and Interpretation!

        ### Summary of our main tasks done to use Streamlit /GitHub

            - we prepared the data set to gain some memory
            - we select the road accident from 2012-2015
            - we kept road accident 2016 seperately to compare with our prediction
            - we did run the classification non-linear models: GBC - RFC - KNN - SVC - (XGBOOST?)
            - EDA and Dataviz are using road accidents from 2012 to 2016 
            
        ### Team

        - Deepa
        - Fan
        - Sidi
        Tutoring : Francesco
        
    """
    )

def eda_advanced():
    import pandas as pd
    import pandas_profiling
    import streamlit as st

    from streamlit_pandas_profiling import st_profile_report
    
    
    @st.cache_data
    def load_data(url):
        df = pd.read_csv(url)
        return df

    df = load_data('https://drive.google.com/file/d/12ZlsdtKvWltFDpO9k6Sv1rhcWEDa3XdT/view?usp=sharing')
    #uploaded_file = st.file_uploader("Choose a file")
    #if uploaded_file is not None:
      #df = pd.read_csv(uploaded_file,low_memory=False)
    pr = df.profile_report()

    st_profile_report(pr)

def data_viz():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import pydeck as pdk
    import plotly.express as px
    import datetime as dt

    from pathlib import Path
    #DATA_URL = Path(Training/Datascientist/Coursera).parents[1] / 'Motor_Vehicle_Collisions_-_Crashes.csv'

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
      DATA_URL = pd.read_csv(uploaded_file,low_memory=False).sample(n=100000)


    df = DATA_URL
    df.dropna(subset=['LATITUDE', 'LONGITUDE','CRASH_DATE','CRASH_TIME'], inplace=True)
    st.title("Road Accident in France")
    st.markdown("This application is a Streamlit dashboard that can be use to analyze road accident in France🗼🥐🇫🇷🥖🚗💥🚙")

    from PIL import Image
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Multi_vehicle_accident_-_M4_Motorway%2C_Sydney%2C_NSW_%288076208846%29.jpg",
                width=600 # Manually Adjust the width of the image as per requirement
            )
    #st.video("https://www.youtube.com/shorts/X5CYrFKcvis")

    df['date/time'] = pd.to_datetime(df['CRASH_DATE'] + ' ' + df['CRASH_TIME'])
    data = df

    #data = load_data(20000)

    #original_data = data

    st.header("Where are the most people injured in France?")
    injured_people = st.slider("Number of person injured in road accident",0, 100)
    st.map(data.query("INJURED_PERSONS >= @injured_people")[['LATITUDE', 'LONGITUDE']].dropna(how="any"))


    st.header("How many road accident during a given time of the day?")
    hour = st.slider("Hour to look at", 0, 23)
    data = data[data['date/time'].dt.hour == hour]


    st.markdown("road accident between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    midpoint = (np.average(data['LATITUDE']), np.average(data['LONGITUDE']))

    st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/streets-v12", initial_view_state={"latitude": midpoint[0],"longitude": midpoint[1],"zoom": 11,"pitch": 50},
         layers=[pdk.Layer("HexagonLayer", data=data[['date/time','LATITUDE','LONGITUDE']], get_position=['LONGITUDE','LATITUDE'], radius=100, extruded=True, pickable=True,
             elevation_scale=4, elevation_range=[0,1000])]))

    st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
    filtered = data[
         (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour +1))
    ]
    hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
    chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
    fig = px.bar(chart_data, x='minute',y='crashes', hover_data=['minute','crashes'], height=400)
    st.write(fig)



    st.header("Top 5 dangerous city by injury type")
    select = st.selectbox('Injured people', ['Pedestrian','Cyclists','Motorists'])

    if select == 'Pedestrian':
        st.write(data.query("INJURED_PEDESTRIANS >= 1")[["ON_STREET_NAME","INJURED_PEDESTRIANS"]].sort_values(by=['INJURED_PEDESTRIANS'], ascending=False).dropna(how='any')[:5])

    elif select == 'Cyclists':
        st.write(data.query("INJURED_CYCLISTS >= 1") [["ON_STREET_NAME","INJURED_CYCLISTS"]].sort_values(by=['INJURED_CYCLISTS'], ascending=False).dropna(how='any')[:5])

    else:
        st.write(data.query("INJURED_MOTORISTS >= 1") [["ON_STREET_NAME","INJURED_MOTORISTS"]].sort_values(by=['INJURED_MOTORISTS'], ascending=False).dropna(how='any')[:5])


        
    if st.checkbox("Show Raw Data", False):
       st.subheader('Raw Data')
       st.write(data)


def modelling():
    import streamlit as st
    import pandas as pd
    from model import prediction, scores

    st.title('Our first Streamlit App')

    st.header('Road Accident in France 2005-2016')

    st.markdown("""Generally speaking we can consider that accuracy scores:
        - Over 90% - Very good
        - Between 70% and 90% - Good
        - Between 60% and 70% - OK""")

    choices = ['Random Forest','SVC','KNN','XGBOOST','Gradient Boosting']

    prediction = st.cache(prediction,suppress_st_warning=True)

    option = st.selectbox(
         'Which model do you want to try ?',
         choices)

    st.write('You selected :', option)

    clf = prediction(option)

    display = st.selectbox(
         "What do you want to display ?",
         ('Accuracy', 'Confusion matrix','Classification report'))

    if display == 'Accuracy':
        st.write(scores(clf, display))
    elif display == 'Confusion matrix':
        st.dataframe(scores(clf, display))
    elif display == 'Classification report':
        #st.table(classification_report(y_test, clf.predict(X_test)))
        st.text(scores(clf, display))

        
page_names_to_funcs = {
    "—": intro,
    "Exploratory Data Analysis advanced": eda_advanced,
    "Exploratory Data Analysis basic": eda_basic,
    "Data Visualization": data_viz,
    "Machine Learning Models": modelling
}

page_name = st.sidebar.selectbox("Choose your page", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
