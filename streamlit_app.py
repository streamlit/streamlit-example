#chatbot with langchain

import streamlit as st
from langchain.llms import OpenAI

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)


# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title('Uber pickups in NYC')

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache_data)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)


# # import altair as alt
# # import numpy as np
# # import pandas as pd
# # import streamlit as st

# # """
# # # Welcome to Streamlit!

# # Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
# # If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# # forums](https://discuss.streamlit.io).

# # In the meantime, below is an example of what you can do with just a few lines of code:
# # """

# # num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# # num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# # indices = np.linspace(0, 1, num_points)
# # theta = 2 * np.pi * num_turns * indices
# # radius = indices

# # x = radius * np.cos(theta)
# # y = radius * np.sin(theta)

# # df = pd.DataFrame({
# #     "x": x,
# #     "y": y,
# #     "idx": indices,
# #     "rand": np.random.randn(num_points),
# # })

# # st.altair_chart(alt.Chart(df, height=700, width=700)
# #     .mark_point(filled=True)
# #     .encode(
# #         x=alt.X("x", axis=None),
# #         y=alt.Y("y", axis=None),
# #         color=alt.Color("idx", legend=None, scale=alt.Scale()),
# #         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
# #     ))


# # # """
# # # # My first app
# # # Here's our first attempt at using data to create a table:
# # # """

# # # import streamlit as st
# # # import pandas as pd
# # # df = pd.DataFrame({
# # #   'first column': [1, 2, 3, 4],
# # #   'second column': [10, 20, 30, 40]
# # # })

# # # df
