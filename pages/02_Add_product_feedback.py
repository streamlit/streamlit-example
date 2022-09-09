import streamlit as st

import pandas as pd
import gspread


scope = ['https://www.googleapis.com/auth/drive']



credentials = {
                "type": st.secrets.credentials["type"],
                "project_id": st.secrets.credentials["project_id"],
                "private_key_id": st.secrets.credentials["private_key_id"],
                "private_key": st.secrets.credentials["private_key"], 
                "client_email": st.secrets.credentials["client_email"], 
                "client_id": st.secrets.credentials["client_id"], 
                "auth_uri": st.secrets.credentials["auth_uri"], 
                "token_uri": st.secrets.credentials["token_uri"], 
                "auth_provider_x509_cert_url": st.secrets.credentials["auth_provider_x509_cert_url"], 
                "client_x509_cert_url": st.secrets.credentials["client_x509_cert_url"]
                }

# gc = gspread.service_account(filename='Authentification\key_google.json')
# gc = gspread.service_account(credentials)
gc = gspread.service_account_from_dict(credentials)



#spreadsheet file named "example"
sps = gc.open('Product Portfolio Planning')

product_feedback = sps.get_worksheet_by_id(1479889959)
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


st.sidebar.info("The database is located here: [link](https://docs.google.com/spreadsheets/d/1ah2joFtc8UV1vyT05KFBJT6fe9QJI_ZjI4Jkl32M1DY/edit#gid=1399876879)")


# Get all feedback categories

#ID	Product 	Feature name	Customer / Website / Conference	Feedback	Category	Business value (k NOK) [MIN]	Business value (k NOK) [MAX]	Implementation time (Person months) [MIN]	Implementation time (Person months) [MAX]
import datetime


st.subheader("Add Product Feedback")
st.write('Select the relevant product.')
product = st.selectbox('Select product', (products[1:]), )

if product != None: 
    st.write("Product Selected: ", product)


    df_features = df[df["Product"] == product]
    features = df_features.Feature.to_list()
    

    
    # preset_values = st.selectbox() # value="",
    # if preset_values != "N/A":
    # get the values for the customer 
    # Position, 




    with st.form("my_form"):

        id_val = max_rows = len(feature_feedback.get_all_values())
        # st.write("Id is set to:", id_val)
        
        # product = st.selectbox('Select related product', (products[1:]))

        # Should show features based on product selection. 

        # Define type of source
        col1, col2 = st.columns(2)
        type_of_source = col1.selectbox('Select source type', ("Potential Customer","Existing Customer", "Compeditor", "Website", "Internal"))

        sorce_name = col2.text_input('Name/Link', '', placeholder = 'write the name/link')
        sorce_company = col2.text_input('Company/Org', '', placeholder = 'write the company/Source', autocomplete = "organization")
        sorce_position = col2.selectbox('Select position type', ("N/A","Environmental", "Technical", "Strategic", "Data", "C-suite"))

        #
        feedback = st.text_input('Feedback', '', placeholder = 'Write the feedback recived, or key takeaways' )

        type_of_feedback = st.selectbox('Select feadback type', ("", "Very Positive", "Positive", "Neutral", "Negative", "Very Negative"))


        st.write('(OPTIONAL) If business value estimates exists (K NOK / year), add these here:')
        st.caption('**Note:** If the following inputs are numbers they are added to the value estimations for the product. The "best estimate" is considered together with the confidence value.')

        col1, col2, col3 = st.columns(3)
        min_business_val = col1.text_input('Min Value (KNOK)', "")
        best_business_val = col2.text_input('**Best Estimate (KNOK)**', "")
        max_business_val = col3.text_input('Max Value (KNOK)', "")

        confidence = st.slider('If applicable: How confident are you in the BEST ESTIMATE above?', 0, 10, 5)


        # min_business_val, max_business_val = st.slider('Estimated Business Value (K NOK) from customer per year ', 0.0, 1000.0, (0.0, 0.0))
        # min_time, max_time= st.slider('Estimated implementation time (OPTIONAL, SET IF KNOWN)', 0.0, 12.0, (0.0, 0.0))

        st.write('(OPTIONAL) If the feedback related to features previously added you may select these here.')
        must_haves = st.multiselect('MUST have related features', features)
        


        date = st.date_input( "Date",datetime.datetime.now())

        submitted = st.form_submit_button("Submit")


        if submitted:

            import json

            must_haves = json.dumps(must_haves)
            product_feedback.append_rows(values=[[id_val, product,sorce_name,sorce_company,sorce_position, type_of_source, feedback, type_of_feedback, min_business_val,best_business_val, max_business_val, confidence ,must_haves, str(date)]])
            st.success("Feedback added")

        # Every form must have a submit button.



# with st.expander("Add new feature <--> Product pair"):
#     with st.form("add_feature"):
#         feature_name = st.text_input('Feature Name', '', placeholder = 'descriptive name')
#         product_selected = st.selectbox('Select related product', (products[1:]), )
#         feature_desc = st.text_input('Feature description', '', placeholder = 'Longer description, preferably with why this feature is useful.')


#         suby = st.form_submit_button("Submit")

#         if suby:
#             features_list.append_rows(values=[[feature_name,product_selected,feature_desc]])
#             st.success("Feature added")




#     st.write("If malfunctioning go to https://docs.google.com/spreadsheets/d/1ah2joFtc8UV1vyT05KFBJT6fe9QJI_ZjI4Jkl32M1DY/edit#gid=1152495848")

        


