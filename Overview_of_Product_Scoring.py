from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import plotly.express as px


import pandas as pd
import gspread

import datetime

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


st.sidebar.info("The database is located here: [link](https://docs.google.com/spreadsheets/d/1ah2joFtc8UV1vyT05KFBJT6fe9QJI_ZjI4Jkl32M1DY/edit#gid=1399876879)")



def main_app():







    st.title('Overview of active products')
    st.caption('Change is defined as difference in average during the last month')

    with st.spinner('Loading data and sorting the scoring..'):



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


        sps = gc.open('Product Portfolio Planning')

        product_feedback = sps.get_worksheet_by_id(1479889959)
        data = product_feedback.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        df["Date"] = pd.to_datetime(df["Date"]) 


        product_about = sps.get_worksheet_by_id(1152495848)
        data_prod = product_about.get_all_values()
        headers_prod = data_prod.pop(0)
        df_products = pd.DataFrame(data_prod, columns=headers_prod)

        





        df['Business value (k NOK) [MIN]'] = pd.to_numeric(df['Business value (k NOK) [MIN]'], errors='coerce')
        df['Business value (k NOK) [MAX]'] = pd.to_numeric(df['Business value (k NOK) [MAX]'], errors='coerce')
        df['Business value (k NOK) [BEST]'] = pd.to_numeric(df['Business value (k NOK) [BEST]'], errors='coerce')
        df['Confidence in value [1-10]'] = pd.to_numeric(df['Confidence in value [1-10]'], errors='coerce')



        df_res = df.groupby(['Product']).mean().reset_index()
        df_res['count'] = df.groupby(['Product']).count().reset_index()['ID']
        df_res['must_haves'] = "" # To be done
        df_res.sort_values(by=['count'])



        df_delta = df[df["Date"] <  (datetime.datetime.now() - datetime.timedelta(weeks=4)) ]
        
        df_delta_res = df_delta.groupby(['Product']).mean().reset_index()
        df_delta_res['count'] = df.groupby(['Product']).count().reset_index()['ID']
        df_delta_res['must_haves'] = "" # To be done
        df_delta_res.sort_values(by=['count'])




    # Logic for sorting by score here. 
    
    df_res = df_res.reset_index()  # make sure indexes pair with number of rows
    for index, row in df_res.iterrows():

        # st.write(str(row))

        st.subheader(row['Product'])  



        col1, col2 = st.columns(2)

        try:
            delta_count = int(df_delta_res.loc[index, 'count']) - int(row['count'])
        except Exception as E:
            print( E)
            delta_count = None



        try:
            delta_best = 100* (int(row['Business value (k NOK) [BEST]']) - int(df_delta_res.loc[index, 'Business value (k NOK) [BEST]']) )/ int(df_delta_res.loc[index, 'Business value (k NOK) [BEST]'])
        except Exception as E:
            print(E)
            delta_best = None

        col1.metric("The count of feedback registered", str(row['count']), delta_count)
        col2.metric("The average best business value estimate [kNOK]", str(row['Business value (k NOK) [BEST]']), str(delta_best) + str("%"))

        # st.caption("A total SAM business value of: "+ str(int(int(df_products[df_products["Product"] == row['Product']].iloc[0,2]) * int(row['Business value (k NOK) [BEST]']))) +" K NOK is based on a SAM of " + str( df_products[df_products["Product"] == row['Product']].iloc[0,2]) + " yearly paying customers." )

        st.write('The following score represents the average confidence for the BEST business estimates.')
        st.progress(int(row["Confidence in value [1-10]"]*10))

        with st.expander("See the underlaying input", expanded=False):
            df[df['Product'] == row['Product']]

        st.write("---")

    

    st.subheader("Overview of the current prioritization matrix (PRODUCT)")

    # Here EASE of development of the product need to be added somehow. 
    df_res['Ease of develoment'] = 5 
    set_max_value = 1000
    df_res['Business value score'] = df_res['Business value (k NOK) [BEST]'].apply(lambda business_value: (business_value * 10 / set_max_value) )




    # import random
    # # list of strings
    # val = [f"HE {i}" for i in range(10)]
    # # size = [40 for i in range(10)]
    # lst = [random.randint(0,10) for i in range(10)]

    # # list of int
    # lst2 = [random.randint(0,10) for i in range(10)]

    # lsts_ = zip(val, lst, lst2)
    # # Calling DataFrame constructor after zipping
    # # both lists, with columns specified

    # df = pd.DataFrame(lsts_,
    #             columns =['val','x', 'y'])

    fig = px.scatter(df_res, x="Business value score", y="Ease of develoment", color="Product",  width=700, height=550)

    import base64
    img_file = "background_go_zone.png"
    background = base64.b64encode(open(img_file, 'rb').read())

    fig.update_layout(
                    images= [dict(
                        source='data:image/png;base64,{}'.format(background.decode()),
                        xref="paper", yref="paper",
                        x=0, y=1,
                        sizex=1, sizey=1,
                        xanchor="left",
                        yanchor="top",
                        sizing="stretch",
                        layer="above")])
 

    st.plotly_chart(fig)



    return None 

import pickle

def set_score():

    with st.expander("Set Options"):

        with st.form("set_score"):


            option_sort = st.selectbox('Sort list by', ['Avg Max', 'Avg Min', 'Count', 'Score'] )

            set_max_value = st.text_input('Max value', '', placeholder = 'write (numeric K NOK) value that yields 10')
            set_max_time  = st.text_input('Max time --> Above this yields 0', '', placeholder = 'write (numeric FTE months) value that yields 0')
            must_haves = st.multiselect('Select what types of input are acceptable', ['customer', 'all', 'internal'])
            date = st.date_input( "Set date to see delta values (standard is 1 month) ", datetime.datetime.now())

            suby = st.form_submit_button("Re-run")

            if suby:

                st.success("Nothing has changed. (Not implemented)")


    return None 




if check_password():
    



    main_app()

    set_score()

    
