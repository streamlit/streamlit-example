# %%
import altair as alt
import pandas as pd
import streamlit as st
import pymysql
import googlemaps
import key

pd.set_option('display.max_columns', None)

# Connection
def data_read(query):
      conn = pymysql.connect(host=key.host, user=key.user,
                                              password=key.password, port=key.port, database=key.database
                                              )
      df = pd.read_sql(query, conn)
      conn.close()
      return df
    
    
ls_en = data_read("select * from listings_enriched_final")


for i in range(len(ls_en.columns)):
  if ls_en[ls_en.columns[i]].dtype == 'object' and ls_en.columns[i] != 'cbsatitle':
    ls_en[ls_en.columns[i]] = ls_en[ls_en.columns[i]].str.title()

label = {}
for i in range(len(ls_en.columns)):
    if (ls_en[ls_en.columns[i]].dtype == 'object') or ('bucket' in ls_en.columns[i]):
      ls_en[ls_en.columns[i]].replace('_', ' ', regex=True, inplace=True)
      ls_en[ls_en.columns[i]].replace('Population ', '', regex=True, inplace=True)
      ls_en[ls_en.columns[i]].replace('Income ', '', regex=True, inplace=True)
      ls_en[ls_en.columns[i]].replace('Between ', '', regex=True, inplace=True)
      ls_en[ls_en.columns[i]].replace('And', '-', regex=True, inplace=True)
      label[ls_en.columns[i]] = ls_en[ls_en.columns[i]].unique().tolist()
    elif 'dummy' in ls_en.columns[i] and ('bucket' not in ls_en.columns[i]):
      label[ls_en.columns[i]] = ls_en[ls_en.columns[i]].unique().tolist()
    elif 'final' in ls_en.columns[i]:
      label[ls_en.columns[i]] = ls_en[ls_en.columns[i]].unique().tolist()


st.markdown("<div><h1 style='text-align: center;'>Where should you live?</h1></div>", unsafe_allow_html=True)


output = []

cbsa_param = st.selectbox("Select Geographic Area", options=sorted(label['cbsatitle']))
col1, col2, col3, col4 = st.columns(4)

with col1:
  home_type_param = st.selectbox("Home Type", options=sorted(label['homeType'])) 
  income_param = st.selectbox("Income", options=sorted(label['majority_income_final']))
  bedroom_param = st.select_slider("Num of Bedrooms", options=sorted(label['bedrooms_final']), on_change=None)

with col2:
  price_param = st.selectbox("Ideal Price Range", options=sorted(label['price_bucket']))
  square_feet_param = st.selectbox("Size Preference", options=sorted(label['sqft_buckets_dummy']))
  year_built_param = st.select_slider("Recently-Built Home", options=sorted(label['yearbuilt_buckets_dummy']), on_change=None)

  
with col3:
  age_param = st.selectbox("Age", options=sorted(label['median_age_bucket']))
  education_options_param = st.selectbox("Education level", options=sorted(label['majority_education_final']))
  bathroom_param = st.select_slider("Num of Bathrooms", options=sorted(label['bathrooms_final']), on_change=None)

with col4:
  family_param = st.selectbox("Family-Oriented Neighborhood", options=sorted(label['family_type_dummy']))   
  ind_param = st.selectbox("Occupation", options=sorted(label['majority_industry_final']))
  centrality_param = st.select_slider("Closeness to Downtown", options=sorted(label['centrality_index_dummy']), on_change=None)  
  

if st.button('Predict'):
  
  query = """
  select pred
  from output_test
  where 
  cbsatitle = '{}'
  and bedroom_bucket_dummy = replace(replace(replace(replace(replace(replace(cast('{}' as unsigned),2,1),3,2),4,2),5,2),6,3),7,3)
  and sqft_buckets_dummy = cast('{}' as unsigned) 
  and yearbuilt_buckets_dummy = cast('{}' as unsigned) 
  and family_type_dummy = cast('{}' as unsigned) 
  and centrality_index_dummy = cast('{}' as unsigned)
  
  and price_bucket = lower('{}')
  and homeType = upper('{}')
  and median_age_bucket =lower('{}') 
  and majority_education_final = lower('{}') 
  and majority_income_final = lower('{}')
  """.format(cbsa_param, bedroom_param, 
             square_feet_param, year_built_param, family_param, centrality_param,
             price_param, home_type_param, age_param, education_options_param, 
             income_param)
  
  # if data_read(query)['pred'].values[0] != None:
  #   zipcode = data_read(query)['pred']
  # else:
  zipcode = 22314
    
  # %%
  st.markdown("<div2><h2 style='text-align: center;'>We recommend you live in zipcode " + str(zipcode) + "!</h2><div2>", unsafe_allow_html=True)
  
  ls = data_read("select * from listing where zipcode = {} limit 10".format(zipcode))
  ls['address'] = ls.apply(lambda x: '%s, %s, %s, %s' % (x['streetAddress'], x['city'], x['state'], x['zipcode']), axis=1)
  ls['lat'] = 0
  ls['lon'] = 0
  
  gmaps_key = googlemaps.Client(key=key.api_key)
  
  for i in range(len(ls)):
    g = gmaps_key.geocode(ls['address'][i])
    if g[0]["geometry"]["location"]["lat"] != 0:
      ls['lat'][i] = g[0]["geometry"]["location"]["lat"]
      ls['lon'][i] = g[0]["geometry"]["location"]["lng"]
    
  # %%
  with st.container():
    st.map(ls[['lat', 'lon']])
    
def main():
    pass
  
if __name__ == '__main__':
	main()
 