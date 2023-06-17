import streamlit as st
import base64

st.write("# Road Accidents in France #")
st.sidebar.success("Select pages")   
       
st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Multi_vehicle_accident_-_M4_Motorway%2C_Sydney%2C_NSW_%288076208846%29.jpg",
            width=700 # Manually Adjust the width of the image as per requirement
        )
st.markdown("""
        **👈 Select the page from the dropdown on the left** to select : EDA, Dataviz, Modelling 
        or Shap Interpretation!
         ### Summary of our main tasks done to use Streamlit /GitHub
            - we prepared the data set to gain some memory
            - we select the road accident from 2012-2015
            - we kept road accident 2016 seperately to compare with our prediction
            - we did run the classification non-linear models: GBC - RFC - KNN - SVC - (XGBOOST?)
            - EDA and Dataviz are using road accidents from 2012 to 2016 
            
         ### 
       
        
    """
    )

st.markdown("![Alt Text](https://media.tenor.com/tuArNck3bKwAAAAC/car-crash.gif)")

# To insert textual content 

st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><br>{"In recent years, road accidents have been a significant cause of concern worldwide, leading to tragic loss of life, injuries, and economic burden. France, like many other countries, strives to enhance road safety and reduce the severity of accidents. To achieve this goal, harnessing the power of data science methods has become increasingly important. By utilizing data-driven approaches, we can gain valuable insights into the factors contributing to the severity of road accidents in France. We believe that machine learning and deep learning are good tools to reduce or prevent road accidents by applying preventive actions using AI solutions."}</p><br>', unsafe_allow_html=True)
st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"The objective of this project is to try to predict the severity of road accidents in France using historical data. By analyzing past records, the aim is to develop a predictive model that can estimate the severity of accidents. This project presents an ideal opportunity to encompass all stages of a comprehensive Data Science project. "}</p><br>', unsafe_allow_html=True)
st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"The initial step involves studying and implementing methods to clean the dataset. This process includes identifying and rectifying any errors, inconsistencies, or missing values present in the dataset. By ensuring the dataquality and reliability, subsequent analysis can conduct to a greater model performance accuracy."}</p><br>', unsafe_allow_html=True)
st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"The next step focuses on extracting relevant characteristics from the historical data. This involves examining the various attributes and factors associated with accidents, such as weather conditions, geographical location, and other related information. By identifying the most influential features, the objective is to develop a robust model that can effectively estimate the severity of accidents based on key features."}</p><br><br><br>', unsafe_allow_html=True)
st.markdown(f'<p align="right" font-family: "Times New Roman" style="color:#000000;">{"TEAM - Sidi Niare, Fan Bu, Deepa Nair M S     Tutoring : Francesco"}</p><br>', unsafe_allow_html=True)

