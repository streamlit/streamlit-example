import streamlit as st
import pickle
import os


<<<<<<< HEAD
def main():
    file_list = os.listdir('files_from_streamlit')
    file_name = st.selectbox('Select File', file_list)
=======
with open('test_files/' + file_name, 'rb') as file:
    data = pickle.load(file)
text = data['text']
html = f'<div style="direction: rtl; text-align: right;">{text}</div>'
st.markdown(f"<div style='direction: rtl; text-align: right;'>{html}</div></br>", unsafe_allow_html=True)
>>>>>>> d69ed82d211841482ff5fdb2d1ea5de8c1e8430f

    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    text = data['text']
    html = f'<div style="direction: rtl; text-align: right;">{text}</div>'
    st.markdown(f"<div style='direction: rtl; text-align: right;'>{html}</div></br>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
