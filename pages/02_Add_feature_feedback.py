from turtle import onclick
import streamlit as st

import pandas as pd
import gspread


scope = ['https://www.googleapis.com/auth/drive']


gc = gspread.service_account(filename='Authentification\key_google.json')

#spreadsheet file named "example"
sps = gc.open('Product Portfolio Planning')

# product_feedback = sps.get_worksheet_by_id(1479889959)
feature_feedback = sps.get_worksheet_by_id(1399876879)
products_list = sps.get_worksheet_by_id(1152495848)
features_list = sps.get_worksheet_by_id(1885443752)



# Get all products 
products = list(products_list.col_values(1))


features = list(features_list.col_values(1))
features_products = list(features_list.col_values(2))
df = pd.DataFrame(list(zip(features[1:], features_products[1:])), columns =[features[0], features_products[0]])


def check_if_feature_exists():
    # if feature is not in pre-defined list, create a new feature with the related feature <--> product connection. 
    return True 




# Get all feedback categories

#ID	Product 	Feature name	Customer / Website / Conference	Feedback	Category	Business value (k NOK) [MIN]	Business value (k NOK) [MAX]	Implementation time (Person months) [MIN]	Implementation time (Person months) [MAX]
import datetime


st.subheader("Add Feature Feedback")
st.write('First, select the relevant product.')


product = st.selectbox('Select related product', (products[1:]), )

if product != None: 
    st.write("Product Selected: ", product)


    df_features = df[df["Product"] == product]
    features = df_features.Feature.to_list()
 

    with st.form("my_form"):

        id_val = max_rows = len(feature_feedback.get_all_values())
        # st.write("Id is set to:", id_val)
        
        # product = st.selectbox('Select related product', (products[1:]))

        # Should show features based on product selection. 

        if product: 
            col1, col2 = st.columns(2)
            feature = col1.selectbox('Select related feature', (features))
            feature_type = col2.selectbox('Select Category', ("Not Selected", "Must Have", "Should Have","Could Have","Won't Have"))

        # Define type of source
        col1, col2 = st.columns(2)
        type_of_source = col1.selectbox('Select feadback type', ("Existing Customer","Potential Customer", "Compeditor", "Website", "Internal"))

        source = col2.text_input('Source', '', placeholder = 'write the name/company/website')

        #
        feedback = st.text_input('Feedback', '', placeholder = 'Write the feedback recived, or key takeaways' )


        st.write('(OPTIONAL) If business value estimates exists, add these here:')
        col1, col2 = st.columns(2)
        min_business_val = col1.text_input('Min Value (KNOK)', "")
        max_business_val = col2.text_input('Max Value (KNOK)', "")

        st.write('(OPTIONAL) If development time estimates exists, add these here:')

        col1, col2 = st.columns(2)
        min_time = col1.text_input('Min Value (Person months FTE)', "")
        max_time = col2.text_input('Max Value (Person months FTE)', "")


        # min_business_val, max_business_val = st.slider('Estimated Business Value (K NOK) from customer per year ', 0.0, 1000.0, (0.0, 0.0))
        # min_time, max_time= st.slider('Estimated implementation time (OPTIONAL, SET IF KNOWN)', 0.0, 12.0, (0.0, 0.0))


        date = st.date_input( "Date",datetime.datetime.now())

        submitted = st.form_submit_button("Submit")

        if submitted:
            feature_feedback.append_rows(values=[[id_val, product,feature,type_of_source, source, feedback,feature_type, min_business_val, max_business_val,min_time,max_time,str(date)  ]])
            st.success("Feedback added")

        # Every form must have a submit button.



with st.expander("Add new feature <--> Product pair"):
    with st.form("add_feature"):
        feature_name = st.text_input('Feature Name', '', placeholder = 'descriptive name')
        product_selected = st.selectbox('Select related product', (products[1:]), )
        feature_desc = st.text_input('Feature description', '', placeholder = 'Longer description, preferably with why this feature is useful.')


        suby = st.form_submit_button("Submit")

        if suby:
            features_list.append_rows(values=[[feature_name,product_selected,feature_desc]])
            st.success("Feature added")




    st.write("If malfunctioning go to https://docs.google.com/spreadsheets/d/1ah2joFtc8UV1vyT05KFBJT6fe9QJI_ZjI4Jkl32M1DY/edit#gid=1152495848")

        


