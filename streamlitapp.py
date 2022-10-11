import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
    streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # write your own comment - what does this do?
    return fruityvice_normalized

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit
  
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


streamlit.title("My parents new healthy diner")

streamlit.title("Breakfast Menu")
streamlit.text('🥣: Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗: Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞: Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit choice to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.header("View Our Fruit List - Add Your Favorites")
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):    
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
